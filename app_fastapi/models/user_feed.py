from sqlalchemy import Column, Integer, String
from .base import Base
import logging

logger = logging.getLogger("app_fastapi.models")

class UserFeedProgress(Base):
    __tablename__ = "user_feed_progress"

    user_hash = Column(String, primary_key=True)
    last_seen_id = Column(Integer, default=0)

    def __repr__(self):
        logger.debug(f"UserFeedProgress representation: user_hash={self.user_hash[:5]}..., last_seen_id={self.last_seen_id}")
        return f"<UserFeedProgress(user={self.user_hash[:5]}..., last_seen={self.last_seen_id})>"