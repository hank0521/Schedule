"""應用程式配置設定"""
from pydantic_settings import BaseSettings
from typing import List
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# 載入 .env 檔案 (優先從根目錄載入，如果不存在則從當前目錄)
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()  # 嘗試從當前目錄載入


class Settings(BaseSettings):
    """應用程式設定類別 - 從環境變數讀取"""

    # 應用程式設定
    APP_NAME: str
    DEBUG: bool

    # 資料庫設定
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def DATABASE_URL(self) -> str:
        """資料庫連線字串"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """同步資料庫連線字串 (用於某些特殊情況)"""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # 安全性設定
    SECRET_KEY: str
    API_KEY: str
    ENCRYPTION_KEY: str

    # CORS 設定
    CORS_ORIGINS: str

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """解析 CORS_ORIGINS 為列表"""
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["*"]

    # 日誌設定
    LOG_LEVEL: str
    LOG_FILE_MAX_BYTES: int
    LOG_FILE_BACKUP_COUNT: int

    class Config:
        case_sensitive = True


# 全域設定實例
settings = Settings()
