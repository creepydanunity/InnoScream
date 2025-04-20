from datetime import datetime, timezone, timedelta


def get_bounds(days=1, addition=True):
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
    now = datetime.utcnow()
    week_start = now - timedelta(days=now.weekday())
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)