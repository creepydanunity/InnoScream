# Standard library
import logging

# Third‑party
from sqlalchemy import Column, Integer, String

# Local application
from .base import Base


logger = logging.getLogger("app_fastapi.models")


class UserFeedProgress(Base):
    """
    Tracks the last-seen scream for each user, to serve a personalized feed.

    Attributes:
        user_hash (str): Primary key, hashed identifier of the user.
        last_seen_id (int): ID of the most recently seen scream.

    Methods:
        __repr__(): Return a debug representation showing feed progress.
    """

    __tablename__ = "user_feed_progress"

    user_hash = Column(String, primary_key=True)
    last_seen_id = Column(Integer, default=0)

    def __repr__(self):
        logger.debug(
            f"UserFeedProgress representation: "
            f"user_hash={self.user_hash[:5]}..., "
            f"last_seen_id={self.last_seen_id}"
            )
        return (
            f"<UserFeedProgress(user={self.user_hash[:5]}..., "
            f"last_seen={self.last_seen_id})>"
        )
