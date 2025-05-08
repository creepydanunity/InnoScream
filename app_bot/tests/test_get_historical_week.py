import pytest
from unittest.mock import MagicMock, patch
import httpx
from app_bot.api.api import get_historical_week


@pytest.mark.asyncio
async def test_get_historical_week_success():
    """Test get_historical_week returns top 3 screams on success."""
    mock_response = {
        "posts": [
            {"content": "Scream 1", "votes": 5,
             "meme_url": "http://example.com/meme1"},
            {"content": "Scream 2", "votes": 3,
             "meme_url": "http://example.com/meme2"},
            {"content": "Scream 3", "votes": 4,
             "meme_url": "http://example.com/meme3"},
            {"content": "Scream 4", "votes": 1,
             "meme_url": "http://example.com/meme4"},
        ]
    }

    with patch.object(
        httpx.AsyncClient,
        "get",
        return_value=MagicMock(
            status_code=200,
            json=lambda: mock_response
        )
    ):
        result = await get_historical_week("2023-01")

        assert len(result) == 3
        assert result[0]["content"] == "Scream 1"
        assert result[1]["content"] == "Scream 2"
        assert result[2]["content"] == "Scream 3"
        assert "meme_url" in result[0]


@pytest.mark.asyncio
async def test_get_historical_week_not_found():
    """Test raises ValueError when week not found (404)."""
    with patch.object(httpx.AsyncClient, "get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "Not Found",
                request=MagicMock(),
                response=mock_resp
            )
        )
        mock_get.return_value = mock_resp
        with pytest.raises(ValueError, match="Week not found in archive"):
            await get_historical_week("invalid-week")


@pytest.mark.asyncio
async def test_get_historical_week_error():
    """Test raises HTTPStatusError on server error (500)."""
    with patch.object(
        httpx.AsyncClient,
        "get",
        return_value=MagicMock(
            status_code=500,
            raise_for_status=MagicMock(
                side_effect=httpx.HTTPStatusError(
                    "Internal Server Error",
                    request=MagicMock(),
                    response=MagicMock()
                )
            )
        )
    ):
        with pytest.raises(httpx.HTTPStatusError):
            await get_historical_week("2023-01")


@pytest.mark.asyncio
async def test_get_historical_week_general_exception():
    """Test handles unexpected exceptions and logs error."""
    with patch.object(
        httpx.AsyncClient,
        "get",
        side_effect=Exception("Unexpected error")
    ), patch("app_bot.api.api.logger") as mock_logger:
        with pytest.raises(Exception, match="Unexpected error"):
            await get_historical_week("2023-01")
        mock_logger.error.assert_any_call(
            "Failed to get historical week: Unexpected error",
            exc_info=True
        )
