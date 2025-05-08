# Standard library
import logging

# Local application
from app_fastapi.initializers.engine import engine
from app_fastapi.models import Base

logger = logging.getLogger("app_fastapi")


async def init_db():
    """
    Initialize the database
    Creating all tables defined in the SQLAlchemy models.

    This function:
      - Logs the start of the initialization process.
      - Opens an asynchronous connection to the database engine.
      - Executes the `Base.metadata.create_all` method within transaction
        to create any missing tables based on the model definitions.
      - Logs success or failure of the operation.
      - Propagates any exceptions encountered during setup.

    Raises:
        Exception: If table creation or database connection fails.
    """
    try:
        logger.info("Initializing database")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}",
                     exc_info=True)
        raise
