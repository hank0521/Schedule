"""FastAPI 應用程式進入點"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.routers import health
from app.core.database import init_database, close_database
from app.core.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 啟動時執行
    logger.info("=" * 60)
    logger.info(f"🚀 {settings.APP_NAME} is starting...")
    logger.info(f"📝 Debug mode: {settings.DEBUG}")
    logger.info(f"🗄️  Database: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    logger.info("=" * 60)

    # 初始化資料庫
    await init_database()

    yield

    # 關閉時執行
    logger.info("=" * 60)
    logger.info(f"👋 {settings.APP_NAME} is shutting down...")
    logger.info("=" * 60)

    # 關閉資料庫連線
    await close_database()


# 建立 FastAPI 應用程式
app = FastAPI(
    title=settings.APP_NAME,
    description="自動化排程系統 API - 支援 HTTP/Mail/FTP 排程任務管理與執行",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(health.router)

# 根路徑
@app.get("/", tags=["Root"])
async def root():
    """根路徑 - API 資訊"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "description": "自動化排程系統 API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
