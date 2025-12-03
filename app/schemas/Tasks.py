"""
Schemas for task-related data models and validation.
"""

from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, field_validator
from typing import Optional


def aware_utcnow() -> datetime:
    """Return current UTC time with timezone awareness."""
    return datetime.now(timezone.utc)


class TaskStatus(str, Enum):
    """Enum for task statuses with UPPER_CASE naming style."""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    RUNNING = "running"
    CANCELED = "canceled"
    FAILED = "failed"


class TaskType(str, Enum):
    """Enum for task types with UPPER_CASE naming style."""
    REMINDER = "reminder"
    FILE_CLEANUP = "file_cleanup"


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    task_type: TaskType
    schedule_time: datetime
    title: str
    receiver_email: str
    webhook_url: Optional[str]

    @field_validator("schedule_time")
    @classmethod
    def validate_future_time(cls, v: datetime) -> datetime:
        """Ensure schedule_time is in the future."""
        now = datetime.utcnow()
        if v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        if v <= now:
            raise ValueError("schedule_time must be in the future")
        return v


class TaskResponse(BaseModel):
    """Schema for returning task data."""
    id: str
    user_id: str
    task_type: str
    schedule_time: datetime
    status: str
    title: str
    receiver_email: str

    model_config = {
        "from_attributes": True
    }


__all__ = ["TaskStatus", "TaskType", "TaskCreate", "TaskResponse"]
