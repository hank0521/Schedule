"""加密解密服務模組"""
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional
from app.config import settings
from app.core.logger import get_logger
import base64

logger = get_logger(__name__)


class CryptoService:
    """加密解密服務類別"""

    def __init__(self, encryption_key: Optional[str] = None):
        """
        初始化加密服務

        Args:
            encryption_key: 加密金鑰 (Base64 編碼的 32 bytes),如果為 None 則使用設定檔中的金鑰
        """
        self.encryption_key = encryption_key or settings.ENCRYPTION_KEY
        self._validate_key()
        self.cipher = Fernet(self.encryption_key.encode())

    def _validate_key(self):
        """驗證加密金鑰是否有效"""
        try:
            # 嘗試建立 Fernet 實例來驗證金鑰格式
            Fernet(self.encryption_key.encode())
        except Exception as e:
            logger.error(f"Invalid encryption key: {e}")
            raise ValueError("Invalid encryption key format")

    def encrypt(self, plaintext: str) -> str:
        """
        加密字串

        Args:
            plaintext: 明文字串

        Returns:
            str: 加密後的字串 (Base64 編碼)

        Raises:
            Exception: 加密失敗時拋出例外
        """
        try:
            encrypted_bytes = self.cipher.encrypt(plaintext.encode())
            encrypted_str = encrypted_bytes.decode()
            logger.debug("Encryption successful")
            return encrypted_str
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, ciphertext: str) -> str:
        """
        解密字串

        Args:
            ciphertext: 加密字串 (Base64 編碼)

        Returns:
            str: 解密後的明文字串

        Raises:
            InvalidToken: 解密失敗時拋出例外 (可能是金鑰錯誤或資料損壞)
        """
        try:
            decrypted_bytes = self.cipher.decrypt(ciphertext.encode())
            decrypted_str = decrypted_bytes.decode()
            logger.debug("Decryption successful")
            return decrypted_str
        except InvalidToken:
            logger.error("Decryption failed: Invalid token or key")
            raise
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

    @staticmethod
    def generate_key() -> str:
        """
        產生新的加密金鑰

        Returns:
            str: Base64 編碼的加密金鑰

        Example:
            key = CryptoService.generate_key()
            print(f"New encryption key: {key}")
        """
        key = Fernet.generate_key()
        return key.decode()

    @staticmethod
    def validate_key(key: str) -> bool:
        """
        驗證金鑰是否有效

        Args:
            key: 要驗證的金鑰

        Returns:
            bool: True 表示金鑰有效, False 表示無效
        """
        try:
            Fernet(key.encode())
            return True
        except Exception:
            return False


# 全域加密服務實例
crypto_service = CryptoService()
