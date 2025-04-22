from typing import Optional
from app_fastapi.models.base import Base
from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class Scream(Base):
    __tablename__ = "screams"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    user_hash: Mapped[str] = mapped_column(String, nullable=False)
    meme_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    moderated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    reactions = relationship("Reaction", back_populates="scream", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scream(id={self.id}, content={self.content[:15]}..., user={self.user_hash})>"