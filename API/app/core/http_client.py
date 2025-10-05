"""HTTP 請求客戶端模組"""
import httpx
import asyncio
from typing import Dict, Optional, Any
from app.core.logger import get_logger

logger = get_logger(__name__)


class HTTPClient:
    """HTTP 請求客戶端類別"""

    def __init__(
        self,
        timeout: int = 30,
        retry_count: int = 0,
        retry_interval: int = 5,
        verify_ssl: bool = True
    ):
        """
        初始化 HTTP 客戶端

        Args:
            timeout: 請求超時時間(秒)
            retry_count: 重試次數
            retry_interval: 重試間隔(秒)
            verify_ssl: 是否驗證 SSL 憑證
        """
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_interval = retry_interval
        self.verify_ssl = verify_ssl

    async def _execute_with_retry(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """
        執行 HTTP 請求並支援重試機制

        Args:
            method: HTTP 方法
            url: 請求 URL
            **kwargs: httpx 請求參數

        Returns:
            httpx.Response: HTTP 回應

        Raises:
            httpx.HTTPError: HTTP 請求失敗
        """
        last_exception = None

        for attempt in range(self.retry_count + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self.timeout,
                    verify=self.verify_ssl
                ) as client:
                    logger.info(f"HTTP {method} request to {url} (attempt {attempt + 1}/{self.retry_count + 1})")

                    response = await client.request(method, url, **kwargs)
                    logger.info(f"HTTP {method} response: {response.status_code}")

                    return response

            except httpx.TimeoutException as e:
                last_exception = e
                logger.warning(f"Request timeout on attempt {attempt + 1}: {e}")

            except httpx.RequestError as e:
                last_exception = e
                logger.warning(f"Request error on attempt {attempt + 1}: {e}")

            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")

            # 如果還有重試次數,等待後重試
            if attempt < self.retry_count:
                logger.info(f"Retrying in {self.retry_interval} seconds...")
                await asyncio.sleep(self.retry_interval)

        # 所有重試都失敗
        logger.error(f"All {self.retry_count + 1} attempts failed")
        raise last_exception

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """
        發送 GET 請求

        Args:
            url: 請求 URL
            headers: 請求標頭
            params: 查詢參數

        Returns:
            httpx.Response: HTTP 回應
        """
        return await self._execute_with_retry(
            "GET",
            url,
            headers=headers,
            params=params
        )

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """
        發送 POST 請求

        Args:
            url: 請求 URL
            headers: 請求標頭
            data: 請求 body (字串或表單資料)
            json: JSON 格式的請求 body

        Returns:
            httpx.Response: HTTP 回應
        """
        return await self._execute_with_retry(
            "POST",
            url,
            headers=headers,
            data=data,
            json=json
        )

    async def put(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """
        發送 PUT 請求

        Args:
            url: 請求 URL
            headers: 請求標頭
            data: 請求 body
            json: JSON 格式的請求 body

        Returns:
            httpx.Response: HTTP 回應
        """
        return await self._execute_with_retry(
            "PUT",
            url,
            headers=headers,
            data=data,
            json=json
        )

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """
        發送 DELETE 請求

        Args:
            url: 請求 URL
            headers: 請求標頭

        Returns:
            httpx.Response: HTTP 回應
        """
        return await self._execute_with_retry(
            "DELETE",
            url,
            headers=headers
        )

    async def patch(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> httpx.Response:
        """
        發送 PATCH 請求

        Args:
            url: 請求 URL
            headers: 請求標頭
            data: 請求 body
            json: JSON 格式的請求 body

        Returns:
            httpx.Response: HTTP 回應
        """
        return await self._execute_with_retry(
            "PATCH",
            url,
            headers=headers,
            data=data,
            json=json
        )

    def validate_response(
        self,
        response: httpx.Response,
        expected_status: int = 200
    ) -> bool:
        """
        驗證回應狀態碼是否符合預期

        Args:
            response: HTTP 回應
            expected_status: 預期的狀態碼

        Returns:
            bool: True 表示符合預期, False 表示不符合
        """
        is_valid = response.status_code == expected_status
        if not is_valid:
            logger.warning(
                f"Unexpected status code: {response.status_code}, "
                f"expected: {expected_status}"
            )
        return is_valid
