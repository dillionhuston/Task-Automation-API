
"""CONTAINS SCHEDULE TASK, NOTHING ELSE """

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.tasks import TaskModel
from app.schemas.Tasks import TaskCreate, TaskResponse
from app.utils import get_db
from celery import Celery
from datetime import datetime, timedelta
from app.tasks.tasks import file_cleanup
import os


celery_app = Celery(
    'tasks',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

#scheudle task function
def schedule_task(db: Session, user_id, task_data: TaskCreate):
    new_task = TaskModel(
        user_id = user_id,
        task_type = task_data.task_type,
        schedule_time = task_data.schedule_time,
        status = "scheduled"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    if task_data.task_type == "file_cleanup":
        file_cleanup.apply_async(args=[new_task.id], eta=new_task.schedule_time)
        print(f"task sceduled for {task_data.task_type} ID: {new_task.id} for user {new_task.user_id} time: {new_task.schedule_time}")

    elif task_data.task_type == "reminder":
        print(f"Task sceduled. ID: {new_task.id} for user {new_task.user_id} at {new_task.schedule_time}")
    return TaskResponse.model_validate(new_task)


