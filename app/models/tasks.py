"""SQLAlchemy model for scheduled tasks."""
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String, ForeignKey, UUID, DateTime
from app.dependencies.constants import (
    TASK_STATUS_SCHEDULED,
    taskscheduledefault
)
from .database import Base

class Task(Base):
    """database for user-tasks"""
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    task_type = Column(String, nullable=False)
    schedule_time = Column(DateTime, nullable=False, default=taskscheduledefault)
    status = Column(String, default=TASK_STATUS_SCHEDULED)
    title = Column(String, default="")
