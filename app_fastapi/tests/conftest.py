import os
import pytest
from fastapi.testclient import TestClient
os.environ["DB_FILENAME"] = ":memory:"
from app_fastapi.main import app
from app_fastapi.initializers.engine import get_session as real_get_session
from app_fastapi.models.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DB_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client():
    app.dependency_overrides[real_get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
