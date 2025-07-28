
from app.schemas import StringConstraints, field_validator, enum, BaseModel
import uuid
from datetime import datetime, timezone
from typing import Optional


def aware_utcnow():
    return datetime.now(timezone.utc)

class TaskStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    canceled = "canceled"


class TaskType(str, enum.Enum):
    remider =  "reminder"
    file_cleanup = "file_cleanup"
    

class TaskCreate(BaseModel):
    task_type: TaskType
    schedule_time: datetime

    @field_validator("schedule_time")
    def validate_future_time(cls, v):
        if v <= aware_utcnow():
            raise ValueError("schedule_time must be in the future")
        return v

class TaskResponse(BaseModel):
    id: uuid.uuid4
    user_id: uuid.uuid4
    task_type: TaskType
    schedule_time: datetime
    status: TaskStatus
            

    class Config:
        from_attributes = True  
    
