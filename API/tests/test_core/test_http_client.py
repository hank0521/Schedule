"""HTTP Client 測試"""
import pytest
from app.core.http_client import HTTPClient


@pytest.mark.asyncio
async def test_http_client_get():
    """測試 HTTP GET 請求"""
    client = HTTPClient(timeout=10, retry_count=1)

    # 使用 httpbin.org 作為測試 API
    response = await client.get("https://httpbin.org/get")

    assert response.status_code == 200
    assert client.validate_response(response, 200) is True


@pytest.mark.asyncio
async def test_http_client_post():
    """測試 HTTP POST 請求"""
    client = HTTPClient(timeout=10)

    response = await client.post(
        "https://httpbin.org/post",
        json={"test": "data"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["json"]["test"] == "data"


@pytest.mark.asyncio
async def test_http_client_retry():
    """測試重試機制"""
    client = HTTPClient(timeout=5, retry_count=2, retry_interval=1)

    # 使用一個不存在的 URL 測試重試
    with pytest.raises(Exception):
        await client.get("https://this-domain-does-not-exist-12345.com")
