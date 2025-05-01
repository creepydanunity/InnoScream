from app_fastapi.initializers.engine import engine
from app_fastapi.models import Base
import logging

logger = logging.getLogger("app_fastapi")

async def init_db():
    try:
        logger.info("Initializing database")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
        raise