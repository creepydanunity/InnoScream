from app_fastapi.models.base import Base
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime


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
        return f"<Reaction({self.emoji}) on Scream {self.scream_id}>"