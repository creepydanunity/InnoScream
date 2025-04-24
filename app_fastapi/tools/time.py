from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger("app_fastapi.tools")

def get_bounds(days=1, addition=True):
    try:
        now = datetime.now(timezone.utc)
        if addition:
            result = (
                now.replace(hour=0, minute=0, second=0, microsecond=0),
                now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days)
            )
        else:
            result = (
                now.replace(hour=0, minute=0, second=0, microsecond=0),
                now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
            )
        logger.debug(f"Calculated time bounds: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to calculate time bounds: {str(e)}", exc_info=True)
        raise

def get_week_start():
    try:
        now = datetime.now(timezone.utc)
        week_start = now - timedelta(days=now.weekday())
        result = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        logger.debug(f"Calculated week start: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to calculate week start: {str(e)}", exc_info=True)
        raise