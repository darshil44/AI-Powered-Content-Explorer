import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_session
from app.core.config import settings
import asyncio

TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/test_db"

engine_test = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
TestingSessionLocal = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
   
    from app.models import SQLModel
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture()
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture()
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


class MockRedis:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ex=None):
        self.store[key] = value

@pytest.fixture()
async def redis_mock(monkeypatch):
    mock = MockRedis()
    monkeypatch.setattr("app.api.search.redis", mock)
    monkeypatch.setattr("app.api.image.redis", mock)
    monkeypatch.setattr("app.api.dashboard.redis", mock)
    yield mock
