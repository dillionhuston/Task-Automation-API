# pylint: disable=too-few-public-methods
"""SQLAlchemy model for users."""

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models.database import Base

class UserModel(Base):
    """Usermodel for user accounts"""
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    files = relationship("FileModel", back_populates="user")
    is_admin = Column(Boolean, default=False)
# change is to uuid 
