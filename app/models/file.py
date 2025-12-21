"""SQLAlchemy model for uploaded files."""
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..models.database import Base

class FileModel(Base):
    """Database of user-uploaded files"""
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    file_path = Column(String)
    file_hash = Column(String)
    user = relationship("UserModel", back_populates="files")
    nonce = Column(String, nullable=False)
