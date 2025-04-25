import json
from sqlalchemy import select
from app_fastapi.initializers.engine import get_session
from app_fastapi.models.admin import Admin
from app_fastapi.tools.crypt import hash_user_id
from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def admin_middleware(request: Request, session: AsyncSession = Depends(get_session),):

    """
    Checks if the requesting user is an admin.

    Parses the request body to extract `user_id`, hashes it, and verifies 
    its presence in the Admin table. Raises 403 if the user is not an admin.
    Also restores the request body for reuse after reading.

    Args:
        request (Request): Incoming HTTP request.
        session (AsyncSession): Async DB session.

    Raises:
        HTTPException: 400 for invalid JSON, 403 for unauthorized access.
    """

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