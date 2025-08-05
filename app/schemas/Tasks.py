
from app.schemas import StringConstraints, enum, BaseModel
import uuid
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID





class TaskStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    running = "running"
    canceled = "canceled"
    failed = "failed"


class TaskType(str, enum.Enum):
    reminder =  "reminder"
    file_cleanup = "file_cleanup"
    

class TaskCreate(BaseModel):
    task_type: TaskType
    schedule_time: datetime
    title: str
    reciever_email:str
    
    """@field_validator("schedule_time")
    def validate_future_time(cls, v):
            if v <= aware_utcnow():
                raise ValueError("schedule_time must be in the future")
            return v"""

class TaskResponse(BaseModel):
    id: int               
    user_id: UUID         
    task_type: str       
    schedule_time: datetime
    status: str          
    title: str

            

    class Config:
        from_attributes = True  
    


__all__ = [
    "validate_future_time",
    "Config",
    "from_attributes"
]