import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from app_bot.api.api import post_scream


@pytest.mark.asyncio
async def test_post_scream_success(monkeypatch):
    """Test that post_scream returns JSON response on successful POST."""
    expected = {"scream_id": "abc123"}
    fake_response = MagicMock(spec=httpx.Response)
    fake_response.json.return_value = expected

    fake_client = AsyncMock()
    fake_client.post.return_value = fake_response
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None

    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)
    result = await post_scream("Hello", "u1")

    assert result == expected
    fake_client.post.assert_awaited_once_with(
        f"{fake_client.post.call_args.args[0]}",
        json={"content": "Hello", "user_id": "u1"}
    )


@pytest.mark.asyncio
async def test_post_scream_failure(monkeypatch):
    """Test that post_scream raises an exception when the request fails."""
    async def boom(*args, **kwargs):
        raise httpx.ConnectError("boom")

    fake_client = AsyncMock()
    fake_client.post.side_effect = boom
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None

    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)

    with pytest.raises(httpx.ConnectError):
        await post_scream("I am chaos", "u2")
