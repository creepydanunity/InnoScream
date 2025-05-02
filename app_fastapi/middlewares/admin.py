# Standard library
import json
import logging

# Third‑party
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Local application
from app_fastapi.initializers.engine import get_session
from app_fastapi.models.admin import Admin
from app_fastapi.tools.crypt import hash_user_id


logger = logging.getLogger("app_fastapi")

async def admin_middleware(request: Request, session: AsyncSession = Depends(get_session),):
    """
    Check if the requesting user is an admin.

    Parses the request body to extract `user_id`, hashes it, and verifies 
    its presence in the Admin table. Raises 403 if the user is not an admin.
    Also restores the request body for reuse after reading.

    Args:
        request (Request): Incoming HTTP request.
        session (AsyncSession): Async DB session.

    Raises:
        HTTPException: 400 for invalid JSON, 403 for unauthorized access.
    """
    try:
        body_bytes = await request.body()

        try:
            json_data = json.loads(body_bytes)
        except Exception as e:
            logger.warning(f"Invalid JSON in request: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON")

        user_id = json_data.get("user_id")
        if not user_id:
            logger.warning("Missing user_id in request")
            raise HTTPException(status_code=400, detail="Missing user_id")

        logger.debug(f"Checking admin rights for user: {user_id[:5]}...")
        user_hash = hash_user_id(user_id)

        result = await session.execute(select(Admin).where(Admin.user_hash == user_hash))
        admin = result.scalar_one_or_none()

        if admin is None:
            logger.warning(f"Unauthorized admin access attempt by user: {user_id[:5]}...")
            raise HTTPException(status_code=403, detail="Unauthorized: not an admin")

        logger.debug(f"Admin access granted for user: {user_id[:5]}...")
        
        async def receive():
            return {"type": "http.request", "body": body_bytes}
        request._receive = receive
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin middleware error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")