from datetime import datetime, timezone, timedelta


def get_bounds(days=1, addition=True):
    """
    Calculate a time range starting from today's beginning in UTC.

    Args:
        days (int, optional): Number of days to add or subtract from today. Defaults to 1.
        addition (bool, optional): If True, adds days; if False, subtracts days. Defaults to True.

    Returns:
        tuple: A tuple of two `datetime` objects (start, end):
            - start: Today at 00:00:00 UTC.
            - end: Today plus or minus the given number of days at 00:00:00 UTC.
    """

    now = datetime.now(timezone.utc)
    if addition:
        return (
            now.replace(hour=0, minute=0, second=0, microsecond=0),
            now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days)
        )
    else:
        return (
            now.replace(hour=0, minute=0, second=0, microsecond=0),
            now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
        )


def get_week_start():
    """
    Get the UTC datetime corresponding to the start of the current week (Monday at 00:00:00).

    Returns:
        datetime: A timezone-aware datetime object (UTC) for the most recent Monday at midnight.
    """
    
    now = datetime.now(timezone.utc)
    week_start = now - timedelta(days=now.weekday())
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)