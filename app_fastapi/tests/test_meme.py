# Standard library
import random

# Third‑party
import pytest
import httpx
from fastapi import HTTPException

# Local application
from app_fastapi.tools.meme import generate_meme_url, IMGFLIP_API_URL

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

@pytest.fixture(autouse=True)
def fixed_env(monkeypatch):
    """
    Set fixed environment variables and random.choice for deterministic behavior.
    """
    monkeypatch.setenv("IMGFLIP_API_USERNAME", "user")
    monkeypatch.setenv("IMGFLIP_API_PASSWORD", "pass")

    monkeypatch.setattr(random, "choice", lambda lst: lst[0])

class AsyncClientMock:
    def __init__(self, response_json=None, exc=None):
        self._resp = response_json
        self._exc = exc

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def post(self, url, data):
        """
        Simulate httpx.AsyncClient.post: either return DummyResponse or raise.
        """
        assert url == IMGFLIP_API_URL
        if self._exc:
            raise self._exc
        return DummyResponse(self._resp)

@pytest.mark.asyncio
async def test_generate_meme_url_success(monkeypatch):
    """
    When Imgflip API returns success, the URL from the payload is returned.
    """
    payload = {
        "success": True,
        "data": {"url": "https://imgflip.com/fake.jpg"}
    }

    monkeypatch.setattr(httpx, "AsyncClient", lambda: AsyncClientMock(response_json=payload))

    url = await generate_meme_url("hello world testing")
    assert url == "https://imgflip.com/fake.jpg"

@pytest.mark.asyncio
async def test_generate_meme_url_api_error(monkeypatch):
    """
    If Imgflip API returns success=False, raise HTTPException with correct detail.
    """
    payload = {"success": False, "error": "Bad template"}
    monkeypatch.setattr(httpx, "AsyncClient", lambda: AsyncClientMock(response_json=payload))

    with pytest.raises(HTTPException) as exc:
        await generate_meme_url("some content here")
    assert exc.value.status_code == 500
    assert "Meme generation failed: Bad template" in exc.value.detail

@pytest.mark.asyncio
async def test_generate_meme_url_exception(monkeypatch, caplog):
    """
    If an unexpected exception occurs during request, log error and raise HTTPException.
    """
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda: AsyncClientMock(exc=RuntimeError("network down"))
    )
    caplog.set_level("ERROR", logger="app_fastapi.tools")

    with pytest.raises(HTTPException) as exc:
        await generate_meme_url("fail test")
    assert exc.value.status_code == 500
    assert "Failed to generate meme" in exc.value.detail

    assert "Failed to generate meme: network down" in caplog.text
