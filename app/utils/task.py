
"""CONTAINS SCHEDULE TASK, NOTHING ELSE """
from app.tasks.tasks import file_cleanup, send_reminder
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.tasks import Task
from app.schemas.Tasks import TaskCreate, TaskResponse
from app.utils import get_db
from app.utils.celery_instance import celery_app
from datetime import datetime, timedelta
from app.utils.email import send_completion_email, send_email_task, schedule_reminder
import os
import uuid


#scheudle task function
def schedule_task(db: Session, user_id, task_data: TaskCreate):
    new_task = Task(
        user_id = uuid.UUID( user_id),
        task_type = task_data.task_type,
        schedule_time = task_data.schedule_time,
        status = "scheduled",
        title = task_data.title
    )
    db.add(new_task)
    db.commit()
    schedule_reminder(new_task.id, receiver_email="") # set this yourself
    db.refresh(new_task)

    from app.tasks.tasks import file_cleanup

    if task_data.task_type == "file_cleanup":
        celery_app.send_task(
            name = "app.tasks.tasks.file_cleanup",
            args=[new_task.id],
            eta=new_task.schedule_time
        )
        print(f"task sceduled for {task_data.task_type} ID: {new_task.id} for user {new_task.user_id} time: {new_task.schedule_time}")
    
    elif task_data.task_type == "reminder":
        celery_app.send_task(
            name = "app.tasks.task.send_reminder",
            args=[new_task.id],
            eta=new_task.schedule_time
        )
        print(f"Task sceduled. ID: {new_task.id} for user {new_task.user_id} at {new_task.schedule_time}")
    return TaskResponse.model_validate(new_task)


