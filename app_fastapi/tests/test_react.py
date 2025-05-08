# Standard library
import asyncio

# Third‑party
import pytest
from sqlalchemy import select

# Local application
from app_fastapi.models.scream import Scream
from app_fastapi.models.reaction import Reaction
from app_fastapi.tools.crypt import hash_user_id
from .conftest import TestingSessionLocal


@pytest.mark.parametrize("missing_id", [999, 123456])
def test_react_not_found(client, missing_id):
    """
    Reacting:
        Non-existent scream ID must return 404 and the correct error message.
    """
    resp = client.post(
        "/react",
        json={"user_id": "user1", "scream_id": missing_id, "emoji": "👍"}
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Scream not found"


def test_react_success_and_duplicate(client):
    """
    A first valid reaction should succeed (200 OK)
    A duplicate reaction by the same user should be rejected (409).
    """
    async def seed_and_test():
        """
        Seed a scream in the database, perform a reaction, verify persistence,
        then test duplicate rejection.
        """
        async with TestingSessionLocal() as session:
            scream = Scream(
                content="Test Scream",
                user_hash=hash_user_id("author")
            )
            session.add(scream)
            await session.commit()
            scream_id = scream.id

        r1 = client.post(
            "/react",
            json={"user_id": "reactor", "scream_id": scream_id, "emoji": "🎉"}
        )
        assert r1.status_code == 200
        assert r1.json()["status"] == "ok"

        async with TestingSessionLocal() as session:
            result = await session.execute(
                select(Reaction).where(
                    Reaction.scream_id == scream_id,
                    Reaction.user_hash == hash_user_id("reactor")
                )
            )
            react_obj = result.scalar_one_or_none()
            assert react_obj is not None
            assert react_obj.emoji == "🎉"

        r2 = client.post(
            "/react",
            json={"user_id": "reactor", "scream_id": scream_id, "emoji": "🎉"}
        )
        assert r2.status_code == 409
        assert r2.json()["detail"] == "Already reacted"

    asyncio.get_event_loop().run_until_complete(seed_and_test())
