from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import tasks
from app.schemas.Tasks import TaskCreate
import os


def schedule_task(db: Session, user_id, task_data: TaskCreate):
    new_task = tasks(
        user_id = user_id,
        task_type = task_data.task_type,
        schedule_time = task_data.schedule_time,
        status = "scheduled"
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    if task_data.task_type == "file_cleanup":
        print(f"reminded sceduled for {task_data.task_type} ID: {new_task.id} for user {new_task.user_id}")

    elif task_data.task_type == "reminder":
        print(f"Task sceduled. ID: {new_task.id} for user {new_task.user_id} at {new_task.schedule_time}")

    return new_task