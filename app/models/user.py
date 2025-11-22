# pylint: disable=too-few-public-methods
"""SQLAlchemy model for users."""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from models.database import Base

class UserModel(Base):
    """User model for user accounts"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    files = relationship("FileModel", back_populates="user")
    is_admin = Column(Boolean, default=False)
