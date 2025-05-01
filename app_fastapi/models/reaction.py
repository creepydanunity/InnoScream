from .base import Base
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import logging

logger = logging.getLogger("app_fastapi.models")

class Reaction(Base):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    emoji: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    scream_id: Mapped[int] = mapped_column(ForeignKey("screams.id", ondelete="CASCADE"))
    user_hash: Mapped[str] = mapped_column(String, nullable=False)

    scream = relationship("Scream", back_populates="reactions")

    __table_args__ = (
        UniqueConstraint("scream_id", "user_hash", name="one_reaction_per_user_per_post"),
    )

    def __repr__(self):
        logger.debug(f"Reaction representation: id={self.id}, emoji={self.emoji}, scream_id={self.scream_id}")
        return f"<Reaction({self.emoji}) on Scream {self.scream_id}>"

    def __str__(self):
        logger.debug(f"Reaction string representation: id={self.id}")
        return f"Reaction(id={self.id}, emoji={self.emoji})"