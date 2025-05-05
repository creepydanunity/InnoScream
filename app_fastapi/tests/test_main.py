import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app_fastapi.main import app, startup
import os


@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"DEFAULT_ADMIN_ID": "admin12345"}):
        yield


@pytest.mark.asyncio
async def test_scheduler_startup():
    with patch("app_fastapi.main.AsyncIOScheduler") as mock_scheduler:
        with patch("app_fastapi.main.init_db", return_value=None):
            await startup()
        # Ensure scheduler is started
        mock_scheduler.assert_called_once()
        mock_scheduler.return_value.add_job.assert_called_once()
        mock_scheduler.return_value.start.assert_called_once()


@pytest.mark.asyncio
async def test_startup_missing_default_admin_id():
    with patch.dict(os.environ, {"DEFAULT_ADMIN_ID": ""}):
        with patch("app_fastapi.main.init_db", return_value=None):
            with patch("app_fastapi.main.logger") as mock_logger:
                await startup()
                mock_logger.warning.assert_called_with(
                    "DEFAULT_ADMIN_ID not found in .env"
                    )


@pytest.mark.asyncio
async def test_startup_failure_handling():
    with patch("app_fastapi.main.init_db",
               side_effect=Exception("DB initialization failed")):
        with patch("app_fastapi.main.logger") as mock_logger:
            with pytest.raises(Exception):
                await startup()

            mock_logger.critical.assert_called_with(
                "Application startup failed: DB initialization failed",
                exc_info=True)


# Test the application if it returns 404 for an invalid route
def test_app_initialization():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 404
