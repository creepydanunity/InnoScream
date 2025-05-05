import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from app_bot.api.api import get_history


@pytest.mark.asyncio
async def test_get_history_success():
    """
    Test that the get_history function returns the correct list of weeks when the API call is successful.
    """

    mock_response = {"weeks": ["2023-01", "2023-02", "2023-03"]}

    with patch.object(
        httpx.AsyncClient, "get", return_value=MagicMock(status_code=200, json=lambda: mock_response, raise_for_status=MagicMock())
    ):
        result = await get_history()

        assert result == mock_response["weeks"]
        assert "2023-01" in result
        assert "2023-02" in result
        assert "2023-03" in result


@pytest.mark.asyncio
async def test_get_history_api_error():
    """
    Test that the get_history function raises an HTTPStatusError when the API call fails with an HTTP error (e.g., status code 500).
    """

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.HTTPStatusError("Internal Server Error", request=AsyncMock(), response=AsyncMock())
        
        with pytest.raises(httpx.HTTPStatusError):
            await get_history()


@pytest.mark.asyncio
async def test_get_history_connection_error():
    """
    Test that the get_history function raises a RequestError when a connection error occurs during the API call.
    """

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.RequestError("Connection error", request=AsyncMock())
        
        with pytest.raises(httpx.RequestError):
            await get_history()
