"""
Schemas for task-related data models and validation.
"""

from datetime import datetime, timezone
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, field_validator


def aware_utcnow() -> datetime:
    """Return current UTC time with timezone awareness."""
    return datetime.now(timezone.utc)


# pylint: disable=invalid-name
class TaskStatus(str, Enum):
    """Enum for task statuses."""
    scheduled = "scheduled"
    completed = "completed"
    running = "running"
    canceled = "canceled"
    failed = "failed"


# pylint: disable=invalid-name
class TaskType(str, Enum):
    """Enum for task types."""
    reminder = "reminder"
    file_cleanup = "file_cleanup"


# pylint: disable=too-few-public-methods
class TaskCreate(BaseModel):
    """Schema for creating a task."""
    task_type: TaskType
    schedule_time: datetime
    title: str
    receiver_email: str

    @field_validator("schedule_time")
    @classmethod
    def validate_future_time(cls, v: datetime) -> datetime:
        """Ensure schedule_time is in the future."""
        now = datetime.utcnow()  # naive UTC
        if v.tzinfo is not None:
            v = v.replace(tzinfo=None)  # drop tzinfo
        if v <= now:
            raise ValueError("schedule_time must be in the future")
        return v


# pylint: disable=too-few-public-methods
class TaskResponse(BaseModel):
    class TaskResponse(BaseModel):
        id: str
        user_id: str  
        task_type: str
        schedule_time: datetime
        status: str
        title: str

    class Config:
        """Pydantic config to allow attribute access."""
        from_attributes = True
        orm_mode = True


__all__ = [
    "TaskStatus",
    "TaskType",
    "TaskCreate",
    "TaskResponse",
]
