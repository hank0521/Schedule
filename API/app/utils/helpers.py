"""通用輔助函式"""
from datetime import datetime
from typing import Optional, List
from pathlib import Path
from app.core.logger import get_logger

logger = get_logger(__name__)


def parse_datetime(datetime_str: str, format: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    解析日期時間字串

    Args:
        datetime_str: 日期時間字串
        format: 日期時間格式

    Returns:
        datetime: datetime 物件,解析失敗則返回 None

    Example:
        >>> parse_datetime("2025-10-05 12:00:00")
        datetime(2025, 10, 5, 12, 0, 0)
    """
    try:
        return datetime.strptime(datetime_str, format)
    except Exception as e:
        logger.error(f"Failed to parse datetime '{datetime_str}': {e}")
        return None


def format_datetime(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化 datetime 物件為字串

    Args:
        dt: datetime 物件
        format: 輸出格式

    Returns:
        str: 格式化後的日期時間字串

    Example:
        >>> format_datetime(datetime(2025, 10, 5, 12, 0, 0))
        "2025-10-05 12:00:00"
    """
    try:
        return dt.strftime(format)
    except Exception as e:
        logger.error(f"Failed to format datetime: {e}")
        return str(dt)


def split_by_delimiter(text: str, delimiter: str = ";") -> List[str]:
    """
    根據分隔符號分割字串並去除空白

    Args:
        text: 要分割的字串
        delimiter: 分隔符號

    Returns:
        List[str]: 分割後的字串列表

    Example:
        >>> split_by_delimiter("a; b ; c", ";")
        ['a', 'b', 'c']
    """
    if not text:
        return []
    return [item.strip() for item in text.split(delimiter) if item.strip()]


def safe_file_read(file_path: str, encoding: str = "utf-8") -> Optional[str]:
    """
    安全地讀取檔案內容

    Args:
        file_path: 檔案路徑
        encoding: 編碼格式

    Returns:
        str: 檔案內容,讀取失敗則返回 None
    """
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read file '{file_path}': {e}")
        return None


def get_file_size(file_path: str) -> Optional[int]:
    """
    取得檔案大小 (bytes)

    Args:
        file_path: 檔案路徑

    Returns:
        int: 檔案大小,取得失敗則返回 None
    """
    try:
        return Path(file_path).stat().st_size
    except Exception as e:
        logger.error(f"Failed to get file size '{file_path}': {e}")
        return None


def format_file_size(size_bytes: int) -> str:
    """
    格式化檔案大小為可讀格式

    Args:
        size_bytes: 檔案大小 (bytes)

    Returns:
        str: 格式化後的檔案大小 (如 "1.5 MB")

    Example:
        >>> format_file_size(1536)
        "1.5 KB"
        >>> format_file_size(1048576)
        "1.0 MB"
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截斷過長的字串

    Args:
        text: 要截斷的字串
        max_length: 最大長度
        suffix: 截斷後的後綴

    Returns:
        str: 截斷後的字串

    Example:
        >>> truncate_string("This is a very long string", 10)
        "This is..."
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix
