"""Validators 測試"""
import pytest
from app.utils.validators import (
    validate_cron,
    validate_email,
    validate_url,
    validate_http_method,
    validate_port
)


def test_validate_cron():
    """測試 Cron 表達式驗證"""
    # 有效的 Cron 表達式
    assert validate_cron("0 */5 * * *") is True
    assert validate_cron("0 0 * * *") is True
    assert validate_cron("*/15 * * * *") is True

    # 無效的 Cron 表達式
    assert validate_cron("invalid") is False
    assert validate_cron("") is False


def test_validate_email():
    """測試 Email 驗證"""
    # 有效的 Email
    assert validate_email("user@example.com") is True
    assert validate_email("test.user@domain.co.uk") is True

    # 無效的 Email
    assert validate_email("invalid-email") is False
    assert validate_email("@example.com") is False
    assert validate_email("user@") is False


def test_validate_url():
    """測試 URL 驗證"""
    # 有效的 URL
    assert validate_url("https://example.com") is True
    assert validate_url("http://localhost:8000/api") is True
    assert validate_url("ftp://ftp.example.com") is True

    # 無效的 URL
    assert validate_url("not-a-url") is False
    assert validate_url("://example.com") is False


def test_validate_http_method():
    """測試 HTTP 方法驗證"""
    # 有效的方法
    assert validate_http_method("GET") is True
    assert validate_http_method("POST") is True
    assert validate_http_method("put") is True  # 不區分大小寫

    # 無效的方法
    assert validate_http_method("INVALID") is False


def test_validate_port():
    """測試埠號驗證"""
    # 有效的埠號
    assert validate_port(80) is True
    assert validate_port(8000) is True
    assert validate_port(65535) is True

    # 無效的埠號
    assert validate_port(0) is False
    assert validate_port(65536) is False
    assert validate_port(-1) is False
