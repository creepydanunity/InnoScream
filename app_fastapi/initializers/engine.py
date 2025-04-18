from os import getenv
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv("app_fastapi/.env")

databaseUrl = "sqlite+aiosqlite:///./" + getenv("DB_FILENAME")
engine = create_async_engine(databaseUrl, echo=True)
asyncSession = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with asyncSession() as session:
        yield session