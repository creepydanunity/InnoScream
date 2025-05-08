# Standard library
import logging
from datetime import datetime, timezone, timedelta


logger = logging.getLogger("app_fastapi.tools")


def get_bounds(days=1, addition=True):
    """Calculate time range starting from today's beginning in UTC.

    Args:
        days (int): Number of days to add/subtract from today. Default 1.
        addition (bool): If True adds days, False subtracts. Default True.

    Returns:
        tuple: Two datetime objects (start, end):
            - start: Today at 00:00:00 UTC
            - end: Today ± days at 00:00:00 UTC
    """
    try:
        now = datetime.now(timezone.utc)
        today = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        if addition:
            result = (today, today + timedelta(days=days))
        else:
            result = (today, today - timedelta(days=days))
        logger.debug(f"Calculated time bounds: {result}")
        return result
    except Exception as e:
        logger.error(
            f"Failed to calculate time bounds: {str(e)}",
            exc_info=True
        )
        raise


def get_week_start():
    """Get UTC datetime for start of current week (Monday 00:00:00).
    Returns:
        datetime:
            Timezone-aware datetime (UTC) for most recent Monday midnight.
    """
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    return week_start.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
