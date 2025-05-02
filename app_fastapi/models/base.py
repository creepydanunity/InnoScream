# Standard library
import logging

# Third‑party
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


logger = logging.getLogger("app_fastapi.models")

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all ORM models, providing async attributes support."""

    pass