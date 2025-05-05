# Standard library
import asyncio

# Third‑party
from sqlalchemy import select

# Local application
from app_fastapi.models.scream import Scream
from .conftest import TestingSessionLocal  

def test_create_scream_success(client):
    """
    Test that posting to /scream returns status "ok" and the scream is persisted.

    This test:
      - Sends a POST request to create a new scream.
      - Asserts the HTTP response is 200 with status "ok".
      - Queries the test database to verify the new Scream record exists
        with the correct content.
    """
    resp = client.post("/scream", json={"user_id": "u1", "content": "hello"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    scream_id = data["scream_id"]

    async def get_record():
        async with TestingSessionLocal() as session:
            result = await session.execute(select(Scream).where(Scream.id == scream_id))
            return result.scalar_one_or_none()

    scream = asyncio.get_event_loop().run_until_complete(get_record())
    assert scream is not None
    assert scream.content == "hello"