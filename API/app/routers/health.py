"""健康檢查 API Router"""
from fastapi import APIRouter, Depends
from datetime import datetime
from app.schemas.common import HealthCheckResponse, DatabaseHealthResponse
from app.core.database import check_database_connection
from app.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    API 健康檢查

    Returns:
        HealthCheckResponse: 健康狀態資訊
    """
    logger.info("Health check requested")
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@router.get("/health/db", response_model=DatabaseHealthResponse, tags=["Health"])
async def database_health_check():
    """
    資料庫連線健康檢查

    Returns:
        DatabaseHealthResponse: 資料庫連線狀態
    """
    logger.info("Database health check requested")
    is_connected = await check_database_connection()

    if is_connected:
        return DatabaseHealthResponse(
            database_connected=True,
            message="Database connection is healthy"
        )
    else:
        return DatabaseHealthResponse(
            database_connected=False,
            message="Database connection failed"
        )
