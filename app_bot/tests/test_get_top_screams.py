import pytest
import os
import httpx
from unittest.mock import AsyncMock, MagicMock

from app_bot.api.api import get_top_screams


API_URL = os.getenv("API_URL")

@pytest.mark.asyncio
async def test_get_top_screams_success(monkeypatch):
    """
    Test successful response from get_top_screams.

    Steps:
    - Mocks httpx.AsyncClient to return a predefined JSON response.
    - Ensures the result of get_top_screams matches the mocked payload.
    - Asserts that the correct URL is requested exactly once.
    """
    expected = {"posts": [{"content": "X", "votes": 5}]}
    fake_response = MagicMock(spec=httpx.Response)
    fake_response.json.return_value = expected
    fake_client = AsyncMock()
    fake_client.get.return_value = fake_response
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)
    result = await get_top_screams()
    assert result == expected
    fake_client.get.assert_awaited_once_with(f"{API_URL}/top")


@pytest.mark.asyncio
async def test_get_top_screams_http_error(monkeypatch):
    """
    Test error handling in get_top_screams when HTTPStatusError is raised.

    Steps:
    - Mocks httpx.AsyncClient.get to raise HTTPStatusError.
    - Asserts that get_top_screams propagates the exception as expected.
    """
    err = httpx.HTTPStatusError("Oops", request=None, response=MagicMock(status_code=500))
    fake_client = AsyncMock()
    fake_client.get.side_effect = err
    fake_client.__aenter__.return_value = fake_client
    fake_client.__aexit__.return_value = None
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kwargs: fake_client)
    with pytest.raises(httpx.HTTPStatusError):
        await get_top_screams()
