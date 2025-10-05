"""日誌服務模組"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config import settings


def setup_logger(name: str) -> logging.Logger:
    """
    設定並返回 logger 實例

    Args:
        name: logger 名稱 (通常使用 __name__)

    Returns:
        logging.Logger: 配置好的 logger 實例
    """
    logger = logging.getLogger(name)

    # 如果已經配置過,直接返回
    if logger.handlers:
        return logger

    # 設定日誌等級
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    # 建立 logs 目錄
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 格式化器
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (with rotation)
    log_file = log_dir / "schedule_api.log"
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=settings.LOG_FILE_MAX_BYTES,
        backupCount=settings.LOG_FILE_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 防止日誌向上傳播
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    取得 logger 實例 (簡化的接口)

    Args:
        name: logger 名稱

    Returns:
        logging.Logger: logger 實例
    """
    return setup_logger(name)
