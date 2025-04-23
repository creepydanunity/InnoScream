from sqlalchemy import Column, Integer, String
from .base import Base

class UserFeedProgress(Base):
    __tablename__ = "user_feed_progress"

    user_hash = Column(String, primary_key=True)
    last_seen_id = Column(Integer, default=0)
