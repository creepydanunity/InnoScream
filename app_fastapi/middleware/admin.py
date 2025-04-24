from app_fastapi.initializers.engine import get_session
from app_fastapi.models.admin import Admin
from fastapi import HTTPException, Depends, Request
import json
from app_fastapi.tools.crypt import hash_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

logger = logging.getLogger("app_fastapi")

async def admin_middleware(request: Request, session: AsyncSession = Depends(get_session)):
    try:
        body_bytes = await request.body()
        logger.debug("Admin middleware processing request")

        try:
            json_data = json.loads(body_bytes)
        except Exception as e:
            logger.warning(f"Invalid JSON in request: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON")

        user_id = json_data.get("user_id")
        if not user_id:
            logger.warning("Missing user_id in request")
            raise HTTPException(status_code=400, detail="Missing user_id")

        user_hash = hash_user_id(user_id)
        logger.debug(f"Checking admin rights for user hash: {user_hash[:5]}...")

        result = await session.execute(select(Admin).where(Admin.user_hash == user_hash))
        admin = result.scalar_one_or_none()

        if admin is None:
            logger.warning(f"Unauthorized admin access attempt by user {user_id}")
            raise HTTPException(status_code=403, detail="Unauthorized: not an admin")

        logger.debug(f"Admin access granted for user {user_id}")
        
        async def receive():
            return {"type": "http.request", "body": body_bytes}
        request._receive = receive
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin middleware error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")