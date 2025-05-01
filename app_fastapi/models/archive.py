from typing import Optional
from .base import Base
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
import logging

logger = logging.getLogger("app_fastapi.models")

class Archive(Base):
    __tablename__ = "archives"

    id: Mapped[int] = mapped_column(primary_key=True)
    scream_id: Mapped[int] = mapped_column(ForeignKey("screams.id", ondelete="CASCADE"))
    week_id: Mapped[int] = mapped_column(Integer, nullable=False)
    place: Mapped[int] = mapped_column(Integer, nullable=False)

    scream = relationship("Scream", back_populates="archives")

    def __repr__(self):
        logger.debug(f"Archive representation: id={self.id}, scream_id={self.scream_id}")
        return f"<Archive(id={self.id}, scream_id={self.scream_id}, week={self.week_id}, place={self.place})>"