# Standard library
import hashlib
import logging
import os


logger = logging.getLogger("app_fastapi.tools")


def hash_user_id(user_id: int) -> str:
    """
    Compute a salted SHA-256 hash of the given user ID.

    This function:
      - Accepts a numeric user identifier.
      - Converts it to its string representation and encodes it to bytes.
      - Computes the SHA-256 hash and returns the hexadecimal digest.
      - Logs the input and the first few characters of the resulting hash.

    Args:
        user_id (int): The external user identifier to hash.

    Returns:
        str: Hexadecimal salted SHA-256 hash of the input user ID.

    Raises:
        Exception: If any error occurs during hashing,
        it is logged and re-raised.
    """
    USER_ID_SALT = os.getenv("USER_ID_SALT")
    try:
        logger.debug(f"Hashing user ID: {str(user_id)[:6]}")

        if not USER_ID_SALT:
            raise ValueError("USER_ID_SALT not found in environment variables")
        salted_user_id = f"{USER_ID_SALT}{user_id}"

        hashed = hashlib.sha256(salted_user_id.encode()).hexdigest()
        logger.debug(
            f"Hashed result: {salted_user_id[:10]}..., "
            f"Hashed result: {hashed[:5]}..."
        )

        return hashed
    except Exception as e:
        logger.error(f"Failed to hash user ID: {str(e)}", exc_info=True)
        raise
