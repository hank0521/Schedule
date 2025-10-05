"""資料驗證工具"""
import re
from croniter import croniter
from email_validator import validate_email as validate_email_format, EmailNotValidError
from urllib.parse import urlparse
from pathlib import Path
import json
from typing import Optional
from app.core.logger import get_logger

logger = get_logger(__name__)


def validate_cron(cron_expr: str) -> bool:
    """
    驗證 Cron 表達式是否有效

    Args:
        cron_expr: Cron 表達式

    Returns:
        bool: True 表示有效, False 表示無效

    Example:
        >>> validate_cron("0 */5 * * *")
        True
        >>> validate_cron("invalid")
        False
    """
    try:
        croniter(cron_expr)
        return True
    except Exception as e:
        logger.warning(f"Invalid cron expression '{cron_expr}': {e}")
        return False


def validate_email(email: str) -> bool:
    """
    驗證 Email 格式是否有效

    Args:
        email: Email 地址

    Returns:
        bool: True 表示有效, False 表示無效

    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    try:
        validate_email_format(email)
        return True
    except EmailNotValidError as e:
        logger.warning(f"Invalid email '{email}': {e}")
        return False


def validate_url(url: str) -> bool:
    """
    驗證 URL 格式是否有效

    Args:
        url: URL 地址

    Returns:
        bool: True 表示有效, False 表示無效

    Example:
        >>> validate_url("https://example.com/api")
        True
        >>> validate_url("not-a-url")
        False
    """
    try:
        result = urlparse(url)
        # 檢查是否有 scheme 和 netloc
        is_valid = all([result.scheme, result.netloc])
        if not is_valid:
            logger.warning(f"Invalid URL '{url}'")
        return is_valid
    except Exception as e:
        logger.warning(f"Invalid URL '{url}': {e}")
        return False


def validate_file_path(path: str, must_exist: bool = False) -> bool:
    """
    驗證檔案路徑格式是否有效

    Args:
        path: 檔案路徑
        must_exist: 是否必須存在

    Returns:
        bool: True 表示有效, False 表示無效

    Example:
        >>> validate_file_path("/path/to/file.txt")
        True
        >>> validate_file_path("/path/to/file.txt", must_exist=True)
        False  # 如果檔案不存在
    """
    try:
        file_path = Path(path)

        if must_exist and not file_path.exists():
            logger.warning(f"File path does not exist: {path}")
            return False

        return True
    except Exception as e:
        logger.warning(f"Invalid file path '{path}': {e}")
        return False


def validate_json(json_str: str) -> bool:
    """
    驗證 JSON 字串是否有效

    Args:
        json_str: JSON 字串

    Returns:
        bool: True 表示有效, False 表示無效

    Example:
        >>> validate_json('{"key": "value"}')
        True
        >>> validate_json('{invalid}')
        False
    """
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON: {e}")
        return False


def validate_http_method(method: str) -> bool:
    """
    驗證 HTTP 方法是否有效

    Args:
        method: HTTP 方法

    Returns:
        bool: True 表示有效, False 表示無效
    """
    valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    is_valid = method.upper() in valid_methods
    if not is_valid:
        logger.warning(f"Invalid HTTP method: {method}")
    return is_valid


def validate_port(port: int) -> bool:
    """
    驗證埠號是否有效

    Args:
        port: 埠號

    Returns:
        bool: True 表示有效 (1-65535), False 表示無效
    """
    is_valid = 1 <= port <= 65535
    if not is_valid:
        logger.warning(f"Invalid port number: {port}")
    return is_valid
