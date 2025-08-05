
"""CONTAINS SCHEDULE TASK, NOTHING ELSE """
from app.tasks.tasks import file_cleanup
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.tasks import Task
from app.schemas.Tasks import TaskCreate, TaskStatus, TaskResponse, TaskType
from app.utils import get_db
from app.utils.celery_instance import celery_app
from datetime import datetime, timedelta
from app.utils.email import send_completion_email, send_email_task, schedule_reminder
import os
import uuid


#scheudle task function
def schedule_task(db: Session, user_id, task_data: TaskCreate, reciever_email:str)->Task:
    """
    Schedule a new task for a user.
    Args:
        db (Session): Database session.
        user_id (str): User's UUID as string.
        task_data (TaskCreate): Task data payload.
        reciever_email(str): Reciever email
    Returns:
        Task: the created Task instance.
    """
    new_task = Task(
        user_id = uuid.UUID( user_id),
        task_type = task_data.task_type,
        schedule_time = task_data.schedule_time,
        status = TaskStatus.scheduled,
        title = task_data.title
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    from app.tasks.tasks import file_cleanup

    if task_data.task_type == TaskType.file_cleanup:
        celery_app.send_task(
            name = "app.tasks.tasks.file_cleanup",
            args=[str(new_task.id), reciever_email],
            eta=new_task.schedule_time
        )
        print(f"task sceduled for {task_data.task_type} ID: {new_task.id} for user {new_task.user_id} time: {new_task.schedule_time}")
    
    elif task_data.task_type == TaskType.reminder:
        celery_app.send_task(
            name = "app.tasks.task.schedule_reminder",
            args=[str(new_task.id), reciever_email],
            eta=new_task.schedule_time
        )
        print(f"Task sceduled. ID: {new_task.id} for user {new_task.user_id} at {new_task.schedule_time}")
    return TaskResponse.model_validate(new_task)


