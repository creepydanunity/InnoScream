from typing import Optional
from app_fastapi.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class Admin(Base):

    """
    Represents an administrative user in the system.

    Attributes:
        id (int): The unique identifier for the admin user.
        user_hash (str): A hashed value representing the admin's user identity.
    
    Methods:
        __repr__(): Returns a string representation of the Admin object, including
                    its unique identifier and user hash for display purposes.
    
    Table schema:
        - id (Primary Key): Integer, auto-generated unique identifier.
        - user_hash (String, Non-nullable): Hashed value for admin's user identity.
    """

    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    def __repr__(self):
        return f"<Admin(id={self.id}, user={self.user_hash})>"