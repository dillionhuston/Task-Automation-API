from models import Base, Column, String, Integer, relationship, UserModel
class FileModel(Base):
    __tablename__ = "Files"

    id = Column(String, primary_key=True)
    hash = Column(String, nullable=False)
    upload_date = Column(String)
    user_id = Column(Integer)
    filename = Column(String, unique=True, index=True)
    user = relationship(UserModel, back_populates="files")