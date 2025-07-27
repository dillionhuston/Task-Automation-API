
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class FileModel(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    user_id = Column(String, ForeignKey("users.id")) 
    file_path = Column(String) 
    file_hash = Column(String)
    user = relationship("UserModel", back_populates="files")
