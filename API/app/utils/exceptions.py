"""自訂例外類別"""


class ScheduleAPIException(Exception):
    """Schedule API 基礎例外類別"""

    def __init__(self, message: str, detail: str = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class DatabaseError(ScheduleAPIException):
    """資料庫相關錯誤"""
    pass


class HTTPClientError(ScheduleAPIException):
    """HTTP 客戶端錯誤"""
    pass


class FTPClientError(ScheduleAPIException):
    """FTP 客戶端錯誤"""
    pass


class MailClientError(ScheduleAPIException):
    """Mail 客戶端錯誤"""
    pass


class ValidationError(ScheduleAPIException):
    """資料驗證錯誤"""
    pass


class AuthenticationError(ScheduleAPIException):
    """認證錯誤"""
    pass


class NotFoundError(ScheduleAPIException):
    """資源未找到錯誤"""
    pass
