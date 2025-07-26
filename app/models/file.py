
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content_type = Column(String)
    user_id = Column(String, ForeignKey("users.id"))  # 

    user = relationship("UserModel", back_populates="files")
