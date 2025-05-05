import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from app_bot.api.api import get_history


@pytest.mark.asyncio
async def test_get_history_success():
    """Test get_history returns correct weeks list on successful API call."""
    mock_response = {"weeks": ["2023-01", "2023-02", "2023-03"]}

    with patch.object(
        httpx.AsyncClient,
        "get",
        return_value=MagicMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=MagicMock()
        )
    ):
        result = await get_history()

        assert result == mock_response["weeks"]
        assert all(
            week in result for week in ["2023-01", "2023-02", "2023-03"]
            )


@pytest.mark.asyncio
async def test_get_history_api_error():
    """Test get_history raises HTTPStatusError on API failure."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.HTTPStatusError(
            "Internal Server Error",
            request=AsyncMock(),
            response=AsyncMock()
        )
        with pytest.raises(httpx.HTTPStatusError):
            await get_history()


@pytest.mark.asyncio
async def test_get_history_connection_error():
    """Test get_history raises RequestError on connection issues."""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.side_effect = httpx.RequestError(
            "Connection error",
            request=AsyncMock()
        )
        with pytest.raises(httpx.RequestError):
            await get_history()
