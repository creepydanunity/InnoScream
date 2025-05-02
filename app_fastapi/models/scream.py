# Standard library
import logging
from datetime import datetime, timezone
from typing import Optional

# Third‑party
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Local application
from .base import Base


logger = logging.getLogger("app_fastapi.models")

class Scream(Base):
    """
    Represents a user-submitted message ("scream").

    Attributes:
        id (int): Primary key.
        content (str): The text content of the scream.
        timestamp (datetime): When the scream was posted (UTC).
        user_hash (str): Hashed identifier of the posting user.
        meme_url (Optional[str]): URL to a generated meme image.
        moderated (bool): Whether the scream has been reviewed by an admin.
        reactions (List[Reaction]): All reactions on this scream.
        archives (List[Archive]): Archive entries if this scream made a top list.

    Methods:
        __repr__(): Return a debug representation of the Scream instance.
        __str__(): Return a simple string identifier for the Scream instance.
    """

    __tablename__ = "screams"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    user_hash: Mapped[str] = mapped_column(String, nullable=False)
    meme_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    moderated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reactions = relationship("Reaction", back_populates="scream", cascade="all, delete-orphan")
    archives = relationship("Archive", back_populates="scream", cascade="all, delete-orphan")

    def __repr__(self):
        logger.debug(f"Scream representation: id={self.id}, user_hash={self.user_hash[:5]}...")
        return f"<Scream(id={self.id}, content={self.content[:15]}..., user={self.user_hash[:5]}...)>"

    def __str__(self):
        logger.debug(f"Scream string representation: id={self.id}")
        return f"Scream(id={self.id})"