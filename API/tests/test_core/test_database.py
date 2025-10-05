"""測試 DatabaseManager 類"""
import pytest
import pytest_asyncio
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import DatabaseManager, Base
from app.config import settings


# 測試用的 Model
class UserModel(Base):
    __tablename__ = "test_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    age = Column(Integer)


@pytest_asyncio.fixture(scope="session")
async def setup_test_database():
    """建立和清理測試資料庫"""
    test_db_name = f"{settings.POSTGRES_DB}_test"

    # 連接到預設的 postgres 資料庫來建立測試資料庫
    admin_url = settings.DATABASE_URL.replace(f"/{settings.POSTGRES_DB}", "/postgres")
    admin_engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

    # 建立測試資料庫
    async with admin_engine.connect() as conn:
        # 檢查資料庫是否存在
        result = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'")
        )
        exists = result.scalar()

        if not exists:
            # 使用雙引號保留大小寫
            await conn.execute(text(f'CREATE DATABASE "{test_db_name}"'))

    await admin_engine.dispose()

    yield test_db_name

    # 測試結束後保留測試資料庫供下次測試使用
    # 每個測試的 fixture 會負責清理表資料


@pytest_asyncio.fixture
async def test_db_manager(setup_test_database):
    """建立測試用的 DatabaseManager"""
    test_db_name = setup_test_database

    # 使用測試資料庫
    test_db_url = settings.DATABASE_URL.replace(
        settings.POSTGRES_DB,
        test_db_name
    )

    # 創建測試用的 DatabaseManager
    db_manager = DatabaseManager()
    db_manager.engine = create_async_engine(
        test_db_url,
        echo=False,
        future=True,
    )
    db_manager.session_factory = sessionmaker(
        db_manager.engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    # 建立測試表
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield db_manager

    # 清理測試表
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db_manager.close()


class TestDatabaseManager:
    """DatabaseManager 測試類"""

    @pytest.mark.asyncio
    async def test_check_connection(self, test_db_manager):
        """測試資料庫連線檢查"""
        result = await test_db_manager.check_connection()
        assert result is True

    @pytest.mark.asyncio
    async def test_create_single_record(self, test_db_manager):
        """測試新增單筆資料"""
        user = UserModel(name="John Doe", email="john@example.com", age=30)
        created_user = await test_db_manager.create(user)

        assert created_user.id is not None
        assert created_user.name == "John Doe"
        assert created_user.email == "john@example.com"
        assert created_user.age == 30

    @pytest.mark.asyncio
    async def test_create_many_records(self, test_db_manager):
        """測試批次新增多筆資料"""
        users = [
            UserModel(name="User1", email="user1@example.com", age=25),
            UserModel(name="User2", email="user2@example.com", age=28),
            UserModel(name="User3", email="user3@example.com", age=35),
        ]
        created_users = await test_db_manager.create_many(users)

        assert len(created_users) == 3
        assert all(user.id is not None for user in created_users)
        assert created_users[0].name == "User1"
        assert created_users[1].name == "User2"
        assert created_users[2].name == "User3"

    @pytest.mark.asyncio
    async def test_get_by_id(self, test_db_manager):
        """測試根據 ID 查詢資料"""
        # 先新增一筆資料
        user = UserModel(name="Jane Doe", email="jane@example.com", age=25)
        created_user = await test_db_manager.create(user)

        # 根據 ID 查詢
        fetched_user = await test_db_manager.get_by_id(UserModel, created_user.id)

        assert fetched_user is not None
        assert fetched_user.id == created_user.id
        assert fetched_user.name == "Jane Doe"
        assert fetched_user.email == "jane@example.com"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_db_manager):
        """測試查詢不存在的 ID"""
        result = await test_db_manager.get_by_id(UserModel, 99999)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all(self, test_db_manager):
        """測試查詢所有資料"""
        # 新增測試資料
        users = [
            UserModel(name=f"User{i}", email=f"user{i}@example.com", age=20+i)
            for i in range(5)
        ]
        await test_db_manager.create_many(users)

        # 查詢所有資料
        all_users = await test_db_manager.get_all(UserModel)

        assert len(all_users) == 5

    @pytest.mark.asyncio
    async def test_get_all_with_pagination(self, test_db_manager):
        """測試分頁查詢"""
        # 新增測試資料
        users = [
            UserModel(name=f"User{i}", email=f"user{i}@example.com", age=20+i)
            for i in range(10)
        ]
        await test_db_manager.create_many(users)

        # 測試分頁
        page1 = await test_db_manager.get_all(UserModel, skip=0, limit=3)
        page2 = await test_db_manager.get_all(UserModel, skip=3, limit=3)

        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].id != page2[0].id

    @pytest.mark.asyncio
    async def test_get_by_filter(self, test_db_manager):
        """測試條件查詢"""
        # 新增測試資料
        users = [
            UserModel(name="Alice", email="alice@example.com", age=30),
            UserModel(name="Bob", email="bob@example.com", age=25),
            UserModel(name="Charlie", email="charlie@example.com", age=30),
        ]
        await test_db_manager.create_many(users)

        # 根據 age 過濾
        filtered_users = await test_db_manager.get_by_filter(UserModel, age=30)

        assert len(filtered_users) == 2
        assert all(user.age == 30 for user in filtered_users)

    @pytest.mark.asyncio
    async def test_update_record(self, test_db_manager):
        """測試更新資料"""
        # 新增一筆資料
        user = UserModel(name="Original Name", email="original@example.com", age=20)
        created_user = await test_db_manager.create(user)

        # 更新資料
        created_user.name = "Updated Name"
        created_user.age = 25
        updated_user = await test_db_manager.update(created_user)

        assert updated_user.name == "Updated Name"
        assert updated_user.age == 25

        # 驗證資料庫中的資料已更新
        fetched_user = await test_db_manager.get_by_id(UserModel, created_user.id)
        assert fetched_user.name == "Updated Name"
        assert fetched_user.age == 25

    @pytest.mark.asyncio
    async def test_delete_record(self, test_db_manager):
        """測試刪除資料"""
        # 新增一筆資料
        user = UserModel(name="To Be Deleted", email="delete@example.com", age=30)
        created_user = await test_db_manager.create(user)

        # 刪除資料
        result = await test_db_manager.delete(created_user)

        assert result is True

        # 驗證資料已被刪除
        fetched_user = await test_db_manager.get_by_id(UserModel, created_user.id)
        assert fetched_user is None

    @pytest.mark.asyncio
    async def test_delete_by_id(self, test_db_manager):
        """測試根據 ID 刪除資料"""
        # 新增一筆資料
        user = UserModel(name="Delete By ID", email="deleteid@example.com", age=28)
        created_user = await test_db_manager.create(user)

        # 根據 ID 刪除
        result = await test_db_manager.delete_by_id(UserModel, created_user.id)

        assert result is True

        # 驗證資料已被刪除
        fetched_user = await test_db_manager.get_by_id(UserModel, created_user.id)
        assert fetched_user is None

    @pytest.mark.asyncio
    async def test_delete_by_id_not_found(self, test_db_manager):
        """測試刪除不存在的資料"""
        result = await test_db_manager.delete_by_id(UserModel, 99999)
        assert result is False

    @pytest.mark.asyncio
    async def test_count(self, test_db_manager):
        """測試計數功能"""
        # 新增測試資料
        users = [
            UserModel(name="User1", email="user1@example.com", age=30),
            UserModel(name="User2", email="user2@example.com", age=25),
            UserModel(name="User3", email="user3@example.com", age=30),
            UserModel(name="User4", email="user4@example.com", age=35),
        ]
        await test_db_manager.create_many(users)

        # 計算所有資料
        total_count = await test_db_manager.count(UserModel)
        assert total_count == 4

        # 計算符合條件的資料
        age_30_count = await test_db_manager.count(UserModel, age=30)
        assert age_30_count == 2

    @pytest.mark.asyncio
    async def test_execute_query(self, test_db_manager):
        """測試執行原始 SQL 查詢"""
        # 新增測試資料
        user = UserModel(name="Query Test", email="query@example.com", age=40)
        await test_db_manager.create(user)

        # 執行原始查詢
        results = await test_db_manager.execute_query(
            "SELECT * FROM test_users WHERE name = :name",
            {"name": "Query Test"}
        )

        assert len(results) == 1
        assert results[0]["name"] == "Query Test"
        assert results[0]["email"] == "query@example.com"

    @pytest.mark.asyncio
    async def test_execute_scalar(self, test_db_manager):
        """測試執行查詢並返回單一值"""
        # 新增測試資料
        users = [
            UserModel(name=f"User{i}", email=f"user{i}@example.com", age=20+i)
            for i in range(5)
        ]
        await test_db_manager.create_many(users)

        # 查詢總數
        count = await test_db_manager.execute_scalar(
            "SELECT COUNT(*) FROM test_users"
        )

        assert count == 5

    @pytest.mark.asyncio
    async def test_execute_non_query(self, test_db_manager):
        """測試執行非查詢語句"""
        # 新增測試資料
        user = UserModel(name="Before Update", email="before@example.com", age=20)
        created_user = await test_db_manager.create(user)

        # 執行更新語句
        rows_affected = await test_db_manager.execute_non_query(
            "UPDATE test_users SET name = :name WHERE id = :id",
            {"name": "After Update", "id": created_user.id}
        )

        assert rows_affected == 1

        # 驗證更新成功
        updated_user = await test_db_manager.get_by_id(UserModel, created_user.id)
        assert updated_user.name == "After Update"

    @pytest.mark.asyncio
    async def test_session_context_manager(self, test_db_manager):
        """測試 session context manager"""
        async with test_db_manager.get_session() as session:
            user = UserModel(name="Context Test", email="context@example.com", age=25)
            session.add(user)
            await session.commit()
            await session.refresh(user)

            assert user.id is not None

        # 驗證資料已保存
        saved_user = await test_db_manager.get_by_id(UserModel, user.id)
        assert saved_user is not None
        assert saved_user.name == "Context Test"

    @pytest.mark.asyncio
    async def test_session_rollback_on_error(self, test_db_manager):
        """測試錯誤時的 rollback 機制"""
        try:
            async with test_db_manager.get_session() as session:
                user = UserModel(name="Rollback Test", email="rollback@example.com", age=25)
                session.add(user)
                await session.commit()

                # 故意引發錯誤
                raise ValueError("Test error")
        except ValueError:
            pass

        # 驗證資料已保存（因為錯誤發生在 commit 之後）
        users = await test_db_manager.get_all(UserModel)
        assert len(users) == 1
