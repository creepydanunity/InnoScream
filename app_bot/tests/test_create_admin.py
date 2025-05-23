import pytest
from unittest.mock import patch, MagicMock
import httpx
from app_bot.api.api import create_admin


@pytest.mark.asyncio
async def test_create_admin_success():
    """Test admin creation returns success message."""
    mock_response = {
        "status": "success",
        "message": "Admin created successfully"
    }
    with patch.object(
        httpx.AsyncClient,
        'post',
        return_value=MagicMock(
            status_code=200,
            json=lambda: mock_response
        )
    ):
        result = await create_admin("user_123", "user_456")
        assert result == mock_response
        assert result["status"] == "success"
        assert result["message"] == "Admin created successfully"


@pytest.mark.asyncio
async def test_create_admin_failure():
    """Test admin creation raises error on API failure."""
    mock_response = MagicMock(status_code=500)
    mock_request = MagicMock()

    with patch.object(
        httpx.AsyncClient,
        'post',
        side_effect=httpx.HTTPStatusError(
            "Failed request",
            request=mock_request,
            response=mock_response
        )
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await create_admin("user_123", "user_456")
