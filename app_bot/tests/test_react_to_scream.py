import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from app_bot.api.api import react_to_scream


@pytest.mark.asyncio
async def test_react_to_scream_success(monkeypatch):
    """Test successful reaction submission returns parsed JSON."""
    expected = {"status": "ok"}
    fake_response = MagicMock(spec=httpx.Response)
    fake_response.json.return_value = expected

    fake_client = AsyncMock()
    fake_client.post.return_value = fake_response
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)

    result = await react_to_scream(1, "🔥", "u1")
    assert result == expected


@pytest.mark.asyncio
async def test_react_to_scream_error(monkeypatch):
    """Test reaction failure raises and logs the error."""
    async def boom(*args, **kwargs):
        raise httpx.ConnectTimeout("timeout")

    fake_client = AsyncMock()
    fake_client.post.side_effect = boom
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)

    with pytest.raises(httpx.ConnectTimeout):
        await react_to_scream(2, "💀", "u99")
