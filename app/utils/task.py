"""
Contains only the task scheduling function.
"""

from typing import Optional
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.tasks import Task
from app.schemas.tasks import TaskCreate, TaskStatus, TaskResponse
from app.utils.celery_instance import celery_app
from app.utils.logger import SingletonLogger
from app.dependencies.constants import TASK_TYPE_REMINDER, TASK_TYPE_FILE_CLEANUP, TASK_STATUS_SCHEDULED
from app.utils.discord import send_discord_notification

from app.FileManager.fileManager import fileManager



logger = SingletonLogger().get_logger()


async def schedule_task(
    db: Session,
    user_id: str,
    task_data: TaskCreate,
    receiver_email: str,
    webhook_url: str,
    file: Optional[UploadFile] = None)->TaskResponse:
    """
    Schedule a new task in the database and (if reminder) send via Celery.

    Args:
        db (Session): SQLAlchemy DB session
        user_id (str): ID of the user
        task_data (TaskCreate): Task creation data
        receiver_email (str): Receiver email for reminder tasks
        webhook_url: (str): Application webhook url for sending tasks
        file: (Fastapi file obj): File for adding attachments to tasks

    Returns:
        TaskResponse: Pydantic validated task
    """

    file_id = None
    #just double check the file does not exist 
    if file is not None and file.filename:
        # await on the async upload file to finsh
        fm = fileManager(db=db)
        uploaded_file = await fm.uploadFile(user_id=user_id, file=file)
        file_id = uploaded_file['id'] 

    new_task = Task(
        id=str(uuid4()),
        user_id=user_id,
        task_type=task_data.task_type.value,
        schedule_time=task_data.schedule_time,
        status=TaskStatus.SCHEDULED.value,
        receiver_email=receiver_email,
        title=task_data.title,
        file_id=file_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(
        "New task scheduled: %s (ID: %s) for user %s at %s, receiver: %s",
        new_task.task_type,
        new_task.id,
        new_task.user_id,
        new_task.schedule_time,
        new_task.receiver_email,
    )
    send_discord_notification(
        webhook_url=task_data.webhook_url, 
        status=TASK_STATUS_SCHEDULED,
        task_name=task_data.title,
        message=f"Task :{task_data.title} ID:{new_task.id} Scheduled for {new_task.schedule_time}"
        )

    #todo make 
    if task_data.task_type == TASK_TYPE_REMINDER:
        celery_app.send_task(
            name="app.tasks.tasks.send_reminder",
            args=[str(new_task.id),file_id, receiver_email],
            eta=new_task.schedule_time,
            
            )
    elif task_data.task_type == TASK_TYPE_FILE_CLEANUP:
        celery_app.send_task(
            name="app.tasks.tasks.file_cleanup",
            args=[str(new_task.id), receiver_email],
            eta=new_task.schedule_time
        )
    return TaskResponse.model_validate(new_task)
