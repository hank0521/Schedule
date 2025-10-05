"""FTP 客戶端模組 (支援 FTP/FTPS/SFTP)"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple
import aioftp
import paramiko
import asyncio
from app.core.logger import get_logger
import glob
import os

logger = get_logger(__name__)


class BaseFTPClient(ABC):
    """FTP 客戶端抽象基礎類別"""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: Optional[str] = None,
        timeout: int = 30
    ):
        """
        初始化 FTP 客戶端

        Args:
            host: FTP 伺服器位址
            port: FTP 埠號
            username: 使用者名稱
            password: 密碼
            timeout: 連線超時時間(秒)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    @abstractmethod
    async def connect(self):
        """建立連線"""
        pass

    @abstractmethod
    async def disconnect(self):
        """斷開連線"""
        pass

    @abstractmethod
    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        """上傳檔案"""
        pass

    @abstractmethod
    async def download_file(self, remote_path: str, local_path: str) -> bool:
        """下載檔案"""
        pass

    @abstractmethod
    async def list_files(self, remote_dir: str) -> List[str]:
        """列出目錄中的檔案"""
        pass

    @abstractmethod
    async def delete_file(self, remote_path: str) -> bool:
        """刪除檔案"""
        pass

    @abstractmethod
    async def create_directory(self, remote_dir: str) -> bool:
        """建立目錄"""
        pass


class FTPClient(BaseFTPClient):
    """標準 FTP 客戶端"""

    def __init__(self, host: str, port: int = 21, username: str = "anonymous",
                 password: Optional[str] = None, timeout: int = 30, passive_mode: bool = True):
        super().__init__(host, port, username, password, timeout)
        self.passive_mode = passive_mode
        self.client = None

    async def connect(self):
        """建立 FTP 連線"""
        try:
            self.client = aioftp.Client()
            await self.client.connect(self.host, self.port)
            await self.client.login(self.username, self.password or "")

            if self.passive_mode:
                await self.client.make_directory(".")  # 測試被動模式

            logger.info(f"Connected to FTP server: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"FTP connection failed: {e}")
            raise

    async def disconnect(self):
        """斷開 FTP 連線"""
        try:
            if self.client:
                await self.client.quit()
                logger.info("Disconnected from FTP server")
        except Exception as e:
            logger.error(f"FTP disconnection error: {e}")

    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        """上傳檔案到 FTP 伺服器"""
        try:
            local_file = Path(local_path)
            if not local_file.exists():
                logger.error(f"Local file not found: {local_path}")
                return False

            logger.info(f"Uploading {local_path} to {remote_path}")
            await self.client.upload(local_path, remote_path, write_into=True)
            logger.info(f"Upload successful: {local_path} -> {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return False

    async def download_file(self, remote_path: str, local_path: str) -> bool:
        """從 FTP 伺服器下載檔案"""
        try:
            logger.info(f"Downloading {remote_path} to {local_path}")
            await self.client.download(remote_path, local_path, write_into=True)
            logger.info(f"Download successful: {remote_path} -> {local_path}")
            return True
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False

    async def list_files(self, remote_dir: str = ".") -> List[str]:
        """列出遠端目錄中的檔案"""
        try:
            files = []
            async for path, info in self.client.list(remote_dir):
                if info["type"] == "file":
                    files.append(str(path))
            logger.info(f"Listed {len(files)} files in {remote_dir}")
            return files
        except Exception as e:
            logger.error(f"List files failed: {e}")
            return []

    async def delete_file(self, remote_path: str) -> bool:
        """刪除遠端檔案"""
        try:
            await self.client.remove(remote_path)
            logger.info(f"Deleted file: {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Delete file failed: {e}")
            return False

    async def create_directory(self, remote_dir: str) -> bool:
        """建立遠端目錄"""
        try:
            await self.client.make_directory(remote_dir)
            logger.info(f"Created directory: {remote_dir}")
            return True
        except Exception as e:
            logger.error(f"Create directory failed: {e}")
            return False


class SFTPClient(BaseFTPClient):
    """SFTP (SSH File Transfer Protocol) 客戶端"""

    def __init__(self, host: str, port: int = 22, username: str = "root",
                 password: Optional[str] = None, timeout: int = 30):
        super().__init__(host, port, username, password, timeout)
        self.ssh_client = None
        self.sftp_client = None

    async def connect(self):
        """建立 SFTP 連線"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 在異步環境中執行同步的 SSH 連線
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.ssh_client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout
                )
            )

            self.sftp_client = self.ssh_client.open_sftp()
            logger.info(f"Connected to SFTP server: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"SFTP connection failed: {e}")
            raise

    async def disconnect(self):
        """斷開 SFTP 連線"""
        try:
            if self.sftp_client:
                self.sftp_client.close()
            if self.ssh_client:
                self.ssh_client.close()
            logger.info("Disconnected from SFTP server")
        except Exception as e:
            logger.error(f"SFTP disconnection error: {e}")

    async def upload_file(self, local_path: str, remote_path: str) -> bool:
        """上傳檔案到 SFTP 伺服器"""
        try:
            local_file = Path(local_path)
            if not local_file.exists():
                logger.error(f"Local file not found: {local_path}")
                return False

            logger.info(f"Uploading {local_path} to {remote_path}")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.sftp_client.put(local_path, remote_path)
            )
            logger.info(f"Upload successful: {local_path} -> {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return False

    async def download_file(self, remote_path: str, local_path: str) -> bool:
        """從 SFTP 伺服器下載檔案"""
        try:
            logger.info(f"Downloading {remote_path} to {local_path}")
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.sftp_client.get(remote_path, local_path)
            )
            logger.info(f"Download successful: {remote_path} -> {local_path}")
            return True
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False

    async def list_files(self, remote_dir: str = ".") -> List[str]:
        """列出遠端目錄中的檔案"""
        try:
            loop = asyncio.get_event_loop()
            files = await loop.run_in_executor(
                None,
                lambda: self.sftp_client.listdir(remote_dir)
            )
            logger.info(f"Listed {len(files)} files in {remote_dir}")
            return files
        except Exception as e:
            logger.error(f"List files failed: {e}")
            return []

    async def delete_file(self, remote_path: str) -> bool:
        """刪除遠端檔案"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.sftp_client.remove(remote_path)
            )
            logger.info(f"Deleted file: {remote_path}")
            return True
        except Exception as e:
            logger.error(f"Delete file failed: {e}")
            return False

    async def create_directory(self, remote_dir: str) -> bool:
        """建立遠端目錄"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.sftp_client.mkdir(remote_dir)
            )
            logger.info(f"Created directory: {remote_dir}")
            return True
        except Exception as e:
            logger.error(f"Create directory failed: {e}")
            return False


class FTPClientFactory:
    """FTP 客戶端工廠類別"""

    @staticmethod
    def create_client(
        protocol: str,
        host: str,
        port: Optional[int] = None,
        username: str = "anonymous",
        password: Optional[str] = None,
        timeout: int = 30,
        passive_mode: bool = True
    ) -> BaseFTPClient:
        """
        建立 FTP 客戶端實例

        Args:
            protocol: 協定類型 (FTP/FTPS/SFTP)
            host: 伺服器位址
            port: 埠號 (如果為 None 則使用預設值)
            username: 使用者名稱
            password: 密碼
            timeout: 超時時間
            passive_mode: 是否使用被動模式 (僅 FTP)

        Returns:
            BaseFTPClient: FTP 客戶端實例
        """
        protocol = protocol.upper()

        if protocol == "FTP":
            port = port or 21
            return FTPClient(host, port, username, password, timeout, passive_mode)
        elif protocol == "SFTP":
            port = port or 22
            return SFTPClient(host, port, username, password, timeout)
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")


async def upload_files_with_pattern(
    client: BaseFTPClient,
    local_pattern: str,
    remote_dir: str,
    delete_after_upload: bool = False
) -> Tuple[int, int]:
    """
    使用萬用字元上傳多個檔案

    Args:
        client: FTP 客戶端實例
        local_pattern: 本地檔案路徑模式 (支援萬用字元,如 *.txt)
        remote_dir: 遠端目錄
        delete_after_upload: 上傳後是否刪除本地檔案

    Returns:
        Tuple[int, int]: (成功數量, 失敗數量)
    """
    success_count = 0
    failure_count = 0

    try:
        # 找出符合模式的所有檔案
        files = glob.glob(local_pattern)
        logger.info(f"Found {len(files)} files matching pattern: {local_pattern}")

        for local_file in files:
            file_name = os.path.basename(local_file)
            remote_file = f"{remote_dir}/{file_name}"

            # 上傳檔案
            success = await client.upload_file(local_file, remote_file)

            if success:
                success_count += 1
                # 如果需要,刪除本地檔案
                if delete_after_upload:
                    try:
                        os.remove(local_file)
                        logger.info(f"Deleted local file: {local_file}")
                    except Exception as e:
                        logger.error(f"Failed to delete local file {local_file}: {e}")
            else:
                failure_count += 1

        logger.info(f"Upload summary: {success_count} succeeded, {failure_count} failed")

    except Exception as e:
        logger.error(f"Upload with pattern failed: {e}")

    return success_count, failure_count
