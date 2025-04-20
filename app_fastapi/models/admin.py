from typing import Optional
from app_fastapi.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    def __repr__(self):
        return f"<Scream(id={self.id}, content={self.content[:15]}..., user={self.user_hash})>"