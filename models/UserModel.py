from sqlalchemy import Column, String, Integer
from .database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer,nullanble=False,primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)
    is_active = Column(bool, unique=False, default=True)
