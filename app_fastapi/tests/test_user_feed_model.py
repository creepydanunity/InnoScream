# Standard library
import logging

# Local application
from app_fastapi.models.user_feed import UserFeedProgress

logger = logging.getLogger("app_fastapi.models")


def test_user_feed_custom_last_seen(caplog):
    """
    UserFeedProgress repr reflects a custom last_seen_id.
    """
    caplog.set_level("DEBUG", logger="app_fastapi.models")
    u = UserFeedProgress(user_hash="xyz", last_seen_id=42)
    assert u.last_seen_id == 42
    assert repr(u) == (
        "<UserFeedProgress(user=xyz.., "
        "last_seen=42)>"
    ).replace("..", "...")
