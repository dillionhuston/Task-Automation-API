from sqlalchemy import Column, String, DateTime
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