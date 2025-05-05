import pytest
from sqlalchemy import select
from app_fastapi.models.archive import Archive
from app_fastapi.models.scream import Scream
from app_fastapi.tests.conftest import TestingSessionLocal

@pytest.fixture
async def archive_and_scream():
    async with TestingSessionLocal() as session:
        scream = Scream(user_hash="1ywe162", content="Test scream content")
        session.add(scream)
        await session.commit()

        archive = Archive(scream_id=scream.id, week_id=202501, place=1)
        session.add(archive)
        await session.commit()

        stmt = select(Archive).where(Archive.id == archive.id)
        db_archive = await session.execute(stmt)
        
        return db_archive.scalars().first()

async def test_create_archive(archive_and_scream):
    db_archive = archive_and_scream

    assert db_archive is not None
    assert db_archive.scream_id == 1
    assert db_archive.week_id == 202501
    assert db_archive.place == 1

async def test_archive_repr(archive_and_scream):
    db_archive = archive_and_scream

    repr_str = repr(db_archive)
    assert "Archive(id=" in repr_str
    assert "scream_id=2" in repr_str
    assert "week=202501" in repr_str
    assert "place=1" in repr_str

