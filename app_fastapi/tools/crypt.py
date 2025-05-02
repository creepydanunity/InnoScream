import hashlib
import logging

logger = logging.getLogger("app_fastapi.tools")

def hash_user_id(user_id: int) -> str:
    try:
        logger.debug(f"Hashing user ID: {user_id}")
        hashed = hashlib.sha256(str(user_id).encode()).hexdigest()
        logger.debug(f"Hashed result: {hashed[:5]}...")
        return hashed
    except Exception as e:
        logger.error(f"Failed to hash user ID: {str(e)}", exc_info=True)
        raise