# Standard library
import logging
from os import getenv
from typing import AsyncGenerator

# Third‑party
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("app_fastapi")

db_url = getenv("DB_FILENAME") if getenv("DB_FILENAME") else ":memory:"

databaseUrl = "sqlite+aiosqlite:///" + db_url

engine = create_async_engine(databaseUrl, echo=True)
asyncSession = sessionmaker(bind=engine, expire_on_commit=False,
                            class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for dependency injection in FastAPI endpoints.

    Yields:
        AsyncSession:
            An asynchronous SQLAlchemy session for interacting with а database.

    Behavior:
        - Creates a new session using the configured async engine.
        - Logs session creation at DEBUG level.
        - Ensures proper cleanup of the session context.
        - Catches and logs any errors during session creation or teardown,
        then propagates them.

    Raises:
        Exception: Re-raises any exception encountered while
        instantiating or closing the session.
    """
    try:
        async with asyncSession() as session:
            logger.debug("Database session created")
            yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}", exc_info=True)
        raise
