from typing import Optional
from .base import Base
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class Archive(Base):
    __tablename__ = "archives"

    id: Mapped[int] = mapped_column(primary_key=True)
    scream_id: Mapped[int] = mapped_column(ForeignKey("screams.id", ondelete="CASCADE"))
    week_id: Mapped[int] = mapped_column(Integer, nullable=False)
    place: Mapped[int] = mapped_column(Integer, nullable=False)

    scream = relationship("Scream", back_populates="archives")