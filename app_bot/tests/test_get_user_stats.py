import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from app_bot.api.api import get_user_stats


@pytest.mark.asyncio
async def test_get_user_stats_success(monkeypatch, caplog):
    """Test that get_user_stats returns parsed JSON on 200 response."""
    expected = {"screams_posted": 5, "reactions_given": 3, "reactions_got": 7}

    fake_response = MagicMock(spec=httpx.Response)
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = expected

    fake_client = AsyncMock()
    fake_client.get.return_value = fake_response
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None

    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)
    with caplog.at_level("DEBUG"):
        result = await get_user_stats("u99")

    assert result == expected
    assert "Getting stats for user u99" in caplog.text or "User stats retrieved successfully" in caplog.text


@pytest.mark.asyncio
async def test_get_user_stats_failure(monkeypatch):
    """Test that get_user_stats raises HTTP error on 404 or server issue."""
    err = httpx.HTTPStatusError("not found", request=None, response=MagicMock(status_code=404))

    fake_client = AsyncMock()
    fake_client.get.side_effect = err
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)

    with pytest.raises(httpx.HTTPStatusError):
        await get_user_stats("ghost")
