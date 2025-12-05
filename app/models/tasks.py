"""SQLAlchemy models for Task Automation API: Task and TaskHistory."""
import uuid
from sqlalchemy import ForeignKey

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, UUID
from ..dependencies.constants import TASK_STATUS_SCHEDULED, taskscheduledefault
from .database import Base


class Task(Base):  # pylint: disable=too-few-public-methods
    """Represents a scheduled task for a user."""
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    task_type = Column(String, nullable=False)
    schedule_time = Column(DateTime, nullable=False, default=taskscheduledefault)
    status = Column(String, default=TASK_STATUS_SCHEDULED)
    title = Column(String, default="")
    receiver_email = Column(String, default="")


class TaskHistory(Base):  # pylint: disable=too-few-public-methods
    """Stores the execution history of tasks."""
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    task_type = Column(String)
    status = Column(String)
    executed_at = Column(DateTime, default=datetime.utcnow)
    details = Column(String)  # such as 42 files deleted
