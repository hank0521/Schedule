"""共用 Pydantic Schemas"""
from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from enum import Enum


# 執行狀態列舉
class ExecutionStatus(str, Enum):
    """執行狀態"""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


# 服務類型列舉
class ServiceType(str, Enum):
    """服務類型"""
    HTTP = "HTTP"
    MAIL = "MAIL"
    FTP = "FTP"


# 錯誤回應 Schema
class ErrorResponse(BaseModel):
    """錯誤回應格式"""
    error: str
    message: str
    detail: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid request data",
                "detail": "Field 'url' is required"
            }
        }


# 成功回應 Schema
class SuccessResponse(BaseModel):
    """成功回應格式"""
    success: bool = True
    message: str
    data: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {"id": 1}
            }
        }


# 分頁回應 Schema
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """分頁回應格式"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        }


# 健康檢查回應 Schema
class HealthCheckResponse(BaseModel):
    """健康檢查回應"""
    status: str
    timestamp: str
    version: str = "1.0.0"

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-10-05T12:00:00",
                "version": "1.0.0"
            }
        }


# 資料庫健康檢查回應 Schema
class DatabaseHealthResponse(BaseModel):
    """資料庫健康檢查回應"""
    database_connected: bool
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "database_connected": True,
                "message": "Database connection is healthy"
            }
        }
