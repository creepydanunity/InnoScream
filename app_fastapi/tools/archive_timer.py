from app_fastapi.initializers.engine import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends


def archive_top(session: AsyncSession = Depends(get_session)):
    pass # TODO: Implement