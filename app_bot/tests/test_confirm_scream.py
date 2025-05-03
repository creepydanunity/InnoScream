import pytest
from unittest.mock import patch, MagicMock
import httpx
from app_bot.api.api import confirm_scream

@pytest.mark.asyncio
async def test_confirm_scream_success():
    """
    Should return success response when scream is confirmed successfully.
    """
    mock_response = {"status": "confirmed"}

    with patch.object(
        httpx.AsyncClient, "post", return_value=MagicMock(status_code=200, json=lambda: mock_response)
    ):
        result = await confirm_scream(101, "admin_001")

        assert result == mock_response
        assert result["status"] == "confirmed"

@pytest.mark.asyncio
async def test_confirm_scream_failure():
    """
    Should raise HTTPStatusError on API failure (e.g., 404 or 500).
    """
    mock_response = MagicMock(status_code=404)
    mock_request = MagicMock()

    with patch.object(
        httpx.AsyncClient, "post",
        side_effect=httpx.HTTPStatusError("Request failed", request=mock_request, response=mock_response)
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await confirm_scream(101, "admin_001")
