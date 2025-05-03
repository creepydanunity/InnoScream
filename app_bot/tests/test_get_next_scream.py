import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock

from app_bot.api.api import get_next_scream


@pytest.mark.asyncio
async def test_get_next_scream_success(monkeypatch):
    """Test get_next_scream returns expected scream dict from backend."""
    expected = {"scream_id": 42, "content": "Yell into the void"}

    fake_response = MagicMock(spec=httpx.Response)
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = expected

    fake_client = AsyncMock()
    fake_client.get.return_value = fake_response
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None

    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)
    result = await get_next_scream("user123")

    assert result == expected


@pytest.mark.asyncio
async def test_get_next_scream_error(monkeypatch):
    """Test get_next_scream raises on backend HTTP error."""
    err = httpx.HTTPStatusError("boom", request=None, response=MagicMock(status_code=404))

    fake_client = AsyncMock()
    fake_client.get.side_effect = err
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None

    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)

    with pytest.raises(httpx.HTTPStatusError):
        await get_next_scream("ghost")
