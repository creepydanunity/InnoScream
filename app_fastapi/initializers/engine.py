from os import getenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger("app_fastapi")

databaseUrl = "sqlite+aiosqlite:///./" + getenv("DB_FILENAME")
logger.debug(f"Database URL: {databaseUrl}")

engine = create_async_engine(databaseUrl, echo=True)
asyncSession = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with asyncSession() as session:
            logger.debug("Database session created")
            yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}", exc_info=True)
        raise