import os
import pytest
from app_fastapi.main import app
from app_fastapi.initializers.engine import get_session as real_get_session
from app_fastapi.models.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


os.environ["DB_FILENAME"] = ":memory:"

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DB_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False)


async def override_get_session():
    """
    Provide a database session override.

    Used for FastAPI dependency injection during testing.

    Yields:
        AsyncSession: A SQLAlchemy asynchronous session
            connected to the in-memory test database.
    """
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Set up and tear down the test database schema.

    This fixture is automatically used once per test session. It:
    - Creates all tables defined in the SQLAlchemy models before tests run.
    - Drops all tables after all tests complete.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client():
    """
    Provide a test client for making HTTP requests to the FastAPI app.

    Overrides the real database session dependency with an in-memory test
        session.
    Yields:
        TestClient: A FastAPI test client instance configured for testing.
    """
    app.dependency_overrides[real_get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
