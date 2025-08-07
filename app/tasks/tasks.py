import os
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from celery import shared_task

from fastapi import HTTPException, status

from app.models.tasks import Task
from app.utils.celery_instance import celery_app
from app.models.database import SessionLocal
from app.schemas.Tasks import TaskStatus
from app.utils.email import schedule_reminder, send_completion_email
from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    TASK_STATUS_RUNNING, 
    TASK_STATUS_COMPLETED,
    TASK_STATUS_SCHEDULED,
    TASK_STATUS_FAILED,
    FILE_STORAGE_DIR,
    HTTP_STATUS_SERVER_ERROR
)

logger = SingletonLogger().get_logger()


@celery_app.task(name="app.tasks.tasks.file_cleanup")
def file_cleanup(task_id: int, reciever_email: str) -> None:
    """
    Delete files older than 1 day and update task status.

    Args:
        task_id (int): ID of the related task.
        reciever_email (str): Email to notify when done.
    """
    task: Optional[Task] = None

    try:
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()

            if not task:
                logger.warning(f"No task found with ID {task_id}")
                return

            task.status = TASK_STATUS_RUNNING
            db.commit()

            threshold = datetime.now() - timedelta(days=1)

            for file in os.listdir(FILE_STORAGE_DIR):
                filepath = os.path.join(FILE_STORAGE_DIR, file)
                if os.path.isfile(filepath) and datetime.fromtimestamp(os.path.getmtime(filepath)) < threshold:
                    os.remove(filepath)
                    logger.info(f"Deleted old file: {filepath}")

            task.status = TASK_STATUS_COMPLETED
            db.commit()

            send_completion_email(task_id, reciever_email)
            logger.info(f"Sent task completion email to {reciever_email}")

    except Exception as e:
        logger.exception(f"File cleanup failed for task_id={task_id}: {e}")
        if task:
            try:
                with SessionLocal() as db:
                    task.status = TASK_STATUS_COMPLETED
                    db.merge(task)
                    db.commit()
            except Exception as db_error:
                logger.error(f"Failed to update task status after failure: {db_error}")


@celery_app.task(name="app.tasks.task.send_reminder")
def send_reminder(task_id: int, receiver_email: str) -> None:
    """
    Send reminder email for a scheduled task.

    Args:
        task_id (int): ID of the task.
        receiver_email (str): Recipient's email.
    """
    task: Optional[Task] = None

    try:
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()

            if not task:
                logger.warning(f"No task found with ID {task_id}")
                return

            task.status = TASK_STATUS_SCHEDULED
            schedule_reminder(task_id, receiver_email)
            db.commit()

            reminder_time = task.schedule_time
            if reminder_time:
                logger.info(f"[Reminder] Task scheduled for {reminder_time} | Type: {task.task_type}")
            else:
                logger.warning("Task has no schedule_time set.")

            task.status = TASK_STATUS_COMPLETED
            db.commit()

    except Exception as e:
        logger.exception(f"Reminder task failed for ID {task_id}: {e}")
        if task:
            try:
                with SessionLocal() as db:
                    task.status = TASK_STATUS_FAILED
                    db.merge(task)
                    db.commit()
            except Exception as db_error:
                logger.error(f"Failed to update task status after reminder failure: {db_error}")


__all__ = ["shared_task", "send_reminder"]
