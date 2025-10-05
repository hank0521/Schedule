"""資料庫連線管理模組 - 統一管理所有資料庫操作"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.sql import Select, Insert, Update, Delete
from typing import AsyncGenerator, List, Optional, Dict, Any, Type, TypeVar
from contextlib import asynccontextmanager
from app.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# Base class for models
Base = declarative_base()

# TypeVar for generic model type
T = TypeVar('T', bound=Base)


class DatabaseManager:
    """
    資料庫管理器 - 統一封裝所有資料庫操作
    類似於 .NET 中封裝 Dapper 的做法
    """

    def __init__(self):
        """初始化資料庫管理器"""
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            future=True,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        logger.info("DatabaseManager initialized")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        取得資料庫 Session (Context Manager)

        Example:
            async with db_manager.get_session() as session:
                result = await session.execute(query)
        """
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Database session error: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()

    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        執行原始 SQL 查詢並返回結果

        Args:
            query: SQL 查詢語句
            params: 查詢參數

        Returns:
            List[Dict[str, Any]]: 查詢結果列表

        Example:
            results = await db_manager.execute_query(
                "SELECT * FROM users WHERE id = :id",
                {"id": 1}
            )
        """
        async with self.get_session() as session:
            try:
                result = await session.execute(text(query), params or {})
                rows = result.fetchall()
                # 轉換為字典列表
                return [dict(row._mapping) for row in rows]
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                raise

    async def execute_scalar(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        執行查詢並返回單一值

        Args:
            query: SQL 查詢語句
            params: 查詢參數

        Returns:
            Any: 單一值結果

        Example:
            count = await db_manager.execute_scalar(
                "SELECT COUNT(*) FROM users"
            )
        """
        async with self.get_session() as session:
            try:
                result = await session.execute(text(query), params or {})
                return result.scalar()
            except Exception as e:
                logger.error(f"Scalar query failed: {e}")
                raise

    async def execute_non_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        執行非查詢語句 (INSERT/UPDATE/DELETE) 並返回受影響的行數

        Args:
            query: SQL 語句
            params: 參數

        Returns:
            int: 受影響的行數

        Example:
            rows_affected = await db_manager.execute_non_query(
                "UPDATE users SET name = :name WHERE id = :id",
                {"name": "John", "id": 1}
            )
        """
        async with self.get_session() as session:
            try:
                result = await session.execute(text(query), params or {})
                await session.commit()
                return result.rowcount
            except Exception as e:
                logger.error(f"Non-query execution failed: {e}")
                await session.rollback()
                raise

    async def get_by_id(self, model: Type[T], id: int) -> Optional[T]:
        """
        根據 ID 查詢單筆資料

        Args:
            model: Model 類別
            id: 主鍵 ID

        Returns:
            Optional[T]: Model 實例或 None

        Example:
            user = await db_manager.get_by_id(User, 1)
        """
        async with self.get_session() as session:
            try:
                return await session.get(model, id)
            except Exception as e:
                logger.error(f"Get by ID failed: {e}")
                raise

    async def get_all(self, model: Type[T], skip: int = 0, limit: int = 100) -> List[T]:
        """
        查詢所有資料 (支援分頁)

        Args:
            model: Model 類別
            skip: 跳過筆數
            limit: 限制筆數

        Returns:
            List[T]: Model 實例列表

        Example:
            users = await db_manager.get_all(User, skip=0, limit=10)
        """
        async with self.get_session() as session:
            try:
                query = select(model).offset(skip).limit(limit)
                result = await session.execute(query)
                return list(result.scalars().all())
            except Exception as e:
                logger.error(f"Get all failed: {e}")
                raise

    async def get_by_filter(self, model: Type[T], **filters) -> List[T]:
        """
        根據條件查詢資料

        Args:
            model: Model 類別
            **filters: 過濾條件 (欄位名=值)

        Returns:
            List[T]: Model 實例列表

        Example:
            users = await db_manager.get_by_filter(User, name="John", age=30)
        """
        async with self.get_session() as session:
            try:
                query = select(model)
                for key, value in filters.items():
                    query = query.filter(getattr(model, key) == value)
                result = await session.execute(query)
                return list(result.scalars().all())
            except Exception as e:
                logger.error(f"Get by filter failed: {e}")
                raise

    async def create(self, instance: T) -> T:
        """
        新增單筆資料

        Args:
            instance: Model 實例

        Returns:
            T: 新增後的 Model 實例 (包含自動產生的 ID)

        Example:
            user = User(name="John", age=30)
            created_user = await db_manager.create(user)
        """
        async with self.get_session() as session:
            try:
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance
            except Exception as e:
                logger.error(f"Create failed: {e}")
                await session.rollback()
                raise

    async def create_many(self, instances: List[T]) -> List[T]:
        """
        批次新增多筆資料

        Args:
            instances: Model 實例列表

        Returns:
            List[T]: 新增後的 Model 實例列表

        Example:
            users = [User(name="John"), User(name="Jane")]
            created_users = await db_manager.create_many(users)
        """
        async with self.get_session() as session:
            try:
                session.add_all(instances)
                await session.commit()
                for instance in instances:
                    await session.refresh(instance)
                return instances
            except Exception as e:
                logger.error(f"Create many failed: {e}")
                await session.rollback()
                raise

    async def update(self, instance: T) -> T:
        """
        更新單筆資料

        Args:
            instance: 已修改的 Model 實例

        Returns:
            T: 更新後的 Model 實例

        Example:
            user = await db_manager.get_by_id(User, 1)
            user.name = "Updated Name"
            updated_user = await db_manager.update(user)
        """
        async with self.get_session() as session:
            try:
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance
            except Exception as e:
                logger.error(f"Update failed: {e}")
                await session.rollback()
                raise

    async def delete(self, instance: T) -> bool:
        """
        刪除單筆資料

        Args:
            instance: 要刪除的 Model 實例

        Returns:
            bool: True 表示刪除成功

        Example:
            user = await db_manager.get_by_id(User, 1)
            success = await db_manager.delete(user)
        """
        async with self.get_session() as session:
            try:
                await session.delete(instance)
                await session.commit()
                return True
            except Exception as e:
                logger.error(f"Delete failed: {e}")
                await session.rollback()
                raise

    async def delete_by_id(self, model: Type[T], id: int) -> bool:
        """
        根據 ID 刪除資料

        Args:
            model: Model 類別
            id: 主鍵 ID

        Returns:
            bool: True 表示刪除成功, False 表示資料不存在

        Example:
            success = await db_manager.delete_by_id(User, 1)
        """
        async with self.get_session() as session:
            try:
                instance = await session.get(model, id)
                if instance:
                    await session.delete(instance)
                    await session.commit()
                    return True
                return False
            except Exception as e:
                logger.error(f"Delete by ID failed: {e}")
                await session.rollback()
                raise

    async def count(self, model: Type[T], **filters) -> int:
        """
        計算符合條件的資料筆數

        Args:
            model: Model 類別
            **filters: 過濾條件

        Returns:
            int: 資料筆數

        Example:
            count = await db_manager.count(User, age=30)
        """
        async with self.get_session() as session:
            try:
                query = select(model)
                for key, value in filters.items():
                    query = query.filter(getattr(model, key) == value)
                result = await session.execute(query)
                return len(list(result.scalars().all()))
            except Exception as e:
                logger.error(f"Count failed: {e}")
                raise

    async def check_connection(self) -> bool:
        """
        檢查資料庫連線是否正常

        Returns:
            bool: True 表示連線正常
        """
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
                logger.info("Database connection check successful")
                return True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False

    async def close(self):
        """關閉資料庫連線"""
        try:
            await self.engine.dispose()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
            raise


# 全域 DatabaseManager 實例
db_manager = DatabaseManager()


# 依賴注入函式 (用於 FastAPI)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 依賴注入函式

    Example:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with db_manager.get_session() as session:
        yield session


# 便捷函式
async def check_database_connection() -> bool:
    """檢查資料庫連線"""
    return await db_manager.check_connection()


async def init_database():
    """初始化資料庫"""
    logger.info("Database initialization completed")


async def close_database():
    """關閉資料庫連線"""
    await db_manager.close()
