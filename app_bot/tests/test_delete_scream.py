import pytest
from unittest.mock import patch, MagicMock
import httpx
from app_bot.api.api import delete_scream


@pytest.mark.asyncio
async def test_delete_scream_success():
    """Should return success response when scream is deleted."""
    mock_response = {"status": "deleted"}

    with patch.object(
        httpx.AsyncClient,
        "post",
        return_value=MagicMock(
            status_code=200,
            json=lambda: mock_response
        )
    ):
        result = await delete_scream(42, "user_123")

        assert result == mock_response
        assert result["status"] == "deleted"


@pytest.mark.asyncio
async def test_delete_scream_failure():
    """Should raise HTTPStatusError when API responds with error."""
    mock_response = MagicMock(status_code=404)
    mock_request = MagicMock()

    with patch.object(
        httpx.AsyncClient,
        "post",
        side_effect=httpx.HTTPStatusError(
            "Request failed",
            request=mock_request,
            response=mock_response
        )
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await delete_scream(42, "user_123")
