from app_fastapi.initializers.engine import get_session
from app_fastapi.models.admin import Admin
from fastapi import HTTPException, Depends, Request
import json
from app_fastapi.tools.crypt import hash_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def admin_middleware(request: Request, session: AsyncSession = Depends(get_session),):
    body_bytes = await request.body()

    try:
        json_data = json.loads(body_bytes)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    user_id = json_data.get("user_id")

    user_hash = hash_user_id(user_id)

    result = await session.execute(select(Admin).where(Admin.user_hash == user_hash))
    admin = result.scalar_one_or_none()

    if admin is None:
        raise HTTPException(status_code=403, detail="Unauthorized: not an admin")

    async def receive():
        return {"type": "http.request", "body": body_bytes}
    request._receive = receive