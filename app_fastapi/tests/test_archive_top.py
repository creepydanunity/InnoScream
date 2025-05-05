# Standard library
import asyncio
from datetime import datetime, timezone

# Third‑party
import pytest
from sqlalchemy import select, func

# Local application
import app_fastapi.tools.archive_top as archive_module
from app_fastapi.tools.archive_top import archive_top_job
from app_fastapi.models.scream import Scream
from app_fastapi.models.archive import Archive
from .conftest import TestingSessionLocal

@pytest.mark.asyncio
async def test_archive_top_handles_no_reactions(monkeypatch):
    """
    archive_top_job should create no Archive entries when there are no reactions.
    """
    monkeypatch.setattr(archive_module, "asyncSession", TestingSessionLocal)

    fixed_now = datetime(2025, 5, 10, tzinfo=timezone.utc)
    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_now
    monkeypatch.setattr(archive_module, "datetime", FakeDateTime)

    async with TestingSessionLocal() as session:
        session.add(Scream(content="lonely", user_hash="u"))
        await session.commit()

    inner_tasks = []
    monkeypatch.setattr(asyncio, "create_task", lambda coro: inner_tasks.append(coro) or coro)

    archive_top_job()
    await inner_tasks[0]

    async with TestingSessionLocal() as session:
        cnt = await session.scalar(select(func.count(Archive.id)))
    assert cnt == 0
