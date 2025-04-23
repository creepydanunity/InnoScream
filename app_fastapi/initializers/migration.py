from app_fastapi.initializers.engine import engine
from app_fastapi.models import Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)