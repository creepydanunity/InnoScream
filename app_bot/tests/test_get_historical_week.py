import pytest
from unittest.mock import MagicMock, patch
import httpx
from app_bot.api.api import get_historical_week

@pytest.mark.asyncio
async def test_get_historical_week_success():
    """
    Test that the get_historical_week function returns the top 3 screams when the API call is successful.
    """

    mock_response = {
        "posts": [
            {"content": "Scream 1", "votes": 5, "meme_url": "http://example.com/meme1"},
            {"content": "Scream 2", "votes": 3, "meme_url": "http://example.com/meme2"},
            {"content": "Scream 3", "votes": 4, "meme_url": "http://example.com/meme3"},
            {"content": "Scream 4", "votes": 1, "meme_url": "http://example.com/meme4"},
        ]
    }

    with patch.object(
        httpx.AsyncClient, "get", return_value=MagicMock(status_code=200, json=lambda: mock_response)
    ):
        result = await get_historical_week("2023-01")

        assert len(result) == 3
        assert result[0]["content"] == "Scream 1"
        assert result[1]["content"] == "Scream 2"
        assert result[2]["content"] == "Scream 3"
        assert "meme_url" in result[0]


@pytest.mark.asyncio
async def test_get_historical_week_not_found():
    """
    Test that the get_historical_week function raises a ValueError when the week is not found (HTTP status 404).
    """

    with patch.object(httpx.AsyncClient, "get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.raise_for_status = MagicMock(side_effect=httpx.HTTPStatusError("Not Found", request=MagicMock(), response=mock_resp))
        
        mock_get.return_value = mock_resp
        
        with pytest.raises(ValueError, match="Week not found in archive"):
            await get_historical_week("invalid-week")


@pytest.mark.asyncio
async def test_get_historical_week_error():
    """
    Test that the get_historical_week function raises an HTTPStatusError when the API returns a 500 server error.
    """

    with patch.object(
        httpx.AsyncClient, "get", return_value=MagicMock(status_code=500, raise_for_status=MagicMock(side_effect=httpx.HTTPStatusError("Internal Server Error", request=MagicMock(), response=MagicMock())))
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await get_historical_week("2023-01")
