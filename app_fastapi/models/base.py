from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
import logging

logger = logging.getLogger("app_fastapi.models")

class Base(AsyncAttrs, DeclarativeBase):
    pass