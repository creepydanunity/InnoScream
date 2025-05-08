# Standard library
import logging

# Third‑party
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Local application
from .base import Base


logger = logging.getLogger("app_fastapi.models")


class Archive(Base):
    """
    Represents an archived top scream for a given week.

    Attributes:
        id (int): Primary key.
        scream_id (int): Foreign key to the original scream.
        week_id (int): Identifier for the week archive in format.
        place (int): Rank or position in that week's top list.
        scream (Scream): Relationship to the original scream object.
    Methods:
        __repr__(): Returns a string representation of the Archive object,
        including its unique identifier and scream_id for future usage.
    """

    __tablename__ = "archives"

    id: Mapped[int] = mapped_column(primary_key=True)
    scream_id: Mapped[int] = mapped_column(ForeignKey("screams.id",
                                                      ondelete="CASCADE"))
    week_id: Mapped[int] = mapped_column(Integer, nullable=False)
    place: Mapped[int] = mapped_column(Integer, nullable=False)

    scream = relationship("Scream", back_populates="archives")

    def __repr__(self):
        logger.debug(f"Archive representation: id={self.id}, "
                     f"scream_id={self.scream_id}")
        return (
            f"<Archive(id={self.id}, scream_id={self.scream_id}, "
            f"week={self.week_id}, place={self.place})>"
            )
