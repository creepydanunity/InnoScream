import pytest
from fastapi.testclient import TestClient

from app_fastapi.main import app
from app_fastapi.models.scream import Scream
from app_fastapi.models.reaction import Reaction
from .conftest import TestingSessionLocal

client = TestClient(app)


def test_top_no_screams(client):
    resp = client.get("/top")
    assert resp.status_code == 200
    assert resp.json() == {"posts": []}


@pytest.mark.asyncio
async def test_top_excludes_negative(monkeypatch):
    async def fake_gen(content):
        return "url"
    monkeypatch.setattr(
        "app_fastapi.api.endpoints.generate_meme_url", fake_gen
        )

    async with TestingSessionLocal() as session:
        s = Scream(content="neg", user_hash="u0")
        session.add(s)
        await session.commit()
        session.add(Reaction(scream_id=s.id, emoji="❌", user_hash="u0"))
        await session.commit()

    resp = client.get("/top")
    assert resp.status_code == 200
    assert resp.json() == {"posts": []}
