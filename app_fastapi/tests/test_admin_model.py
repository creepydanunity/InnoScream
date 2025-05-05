import pytest
from app_fastapi.models.admin import Admin
from app_fastapi.models.base import Base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from app_fastapi.tests.conftest import TestingSessionLocal
import logging


@pytest.fixture
async def admin_fixture():
    async with TestingSessionLocal() as session:
        admin = Admin(user_hash="hashed_admin_12345")
        session.add(admin)
        await session.commit()

        stmt = select(Admin).where(Admin.id == admin.id)
        db_admin = await session.execute(stmt)

        return db_admin.scalars().first()

async def test_create_admin(admin_fixture):
    db_admin = admin_fixture

    assert db_admin is not None
    assert db_admin.user_hash == "hashed_admin_12345"

async def test_admin_repr(admin_fixture):
    db_admin = admin_fixture

    repr_str = repr(db_admin)
    assert "Admin(id=" in repr_str
    assert "user=hashe..." in repr_str

async def test_admin_str(admin_fixture):
    db_admin = admin_fixture

    str_repr = str(db_admin)
    assert "Admin(id=" in str_repr
    assert f"Admin(id={db_admin.id})" in str_repr
