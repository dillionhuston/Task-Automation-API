# app/models.py or app/models/task.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # make sure this matches __tablename__
    task_type = Column(String, nullable=False)
    schedule_time = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
