from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from .database import Base
from app.dependencies.constants import TASK_STATUS_SCHEDULED, taskscheduledefault


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)        
    user_id = Column(String)                                 
    task_type = Column(String, nullable=False)              
    schedule_time = Column(DateTime, nullable=False, default=taskscheduledefault)
    status = Column(String, default=TASK_STATUS_SCHEDULED)  
    title = Column(String, default="")
    receiver_email = Column(String, default="")



class TaskHistory(Base):
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True, autoincrement=True)  # make sure autoincrement is True
    task_type = Column(String)
    status = Column(String)
    executed_at = Column(DateTime, default=datetime.utcnow)
    details = Column(String) # such as 42 files deleted
