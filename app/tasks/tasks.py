"""
Celery tasks for handling scheduled jobs such as file cleanup and sending reminders.
"""

import os
from typing import Optional
from datetime import datetime, timedelta
from celery import shared_task
from sqlalchemy.orm import Session
import requests

from app.models.tasks import Task, TaskHistory
from app.utils.celery_instance import celery_app
from app.models.database import SessionLocal
from app.utils.email import send_completion_email
from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    TASK_STATUS_RUNNING,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_FAILED,
    FILE_STORAGE_DIR,
)

logger = SingletonLogger().get_logger()


def log_task_history(db: Session, task_type: str, status: str, details: str):
    history = TaskHistory(task_type=task_type, status=status, details=details)
    db.add(history)
    db.commit()

@celery_app.task(name="app.tasks.tasks.file_cleanup")
def file_cleanup(task_id: int, receiver_email: Optional[str] = None) -> None:
    """
    Delete files older than 1 day and update task status.
    """
    task: Optional[Task] = None

    try:
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()

            if not task:
                logger.warning(f"No task found with ID {task_id}")
                return

            # Mark task as running
            task.status = TASK_STATUS_RUNNING
            db.commit()

            threshold = datetime.now() - timedelta(days=1)
            deleted_count = 0

            for file in os.listdir(FILE_STORAGE_DIR):
                filepath = os.path.join(FILE_STORAGE_DIR, file)
                if os.path.isfile(filepath) and datetime.fromtimestamp(os.path.getmtime(filepath)) < threshold:
                    os.remove(filepath)
                    deleted_count += 1

            logger.info(f"Deleted {deleted_count} old files.")

            # Mark task completed
            task.status = TASK_STATUS_COMPLETED
            db.commit()

            details_msg = f"Deleted {deleted_count} files"
            if receiver_email:
                send_completion_email(task_id, receiver_email)
                logger.info(f"Sent task completion email to {receiver_email}")
                details_msg += f", email sent to {receiver_email}"
            else:
                logger.warning(f"Task {task_id} has no receiver_email. No email sent.")
                details_msg += ", no email sent"

            log_task_history(db, task_type="file_cleanup", status="COMPLETED", details=details_msg)

    except Exception as e:
        logger.exception(f"File cleanup failed for task_id={task_id}: {e}")

        if task:
            try:
                with SessionLocal() as db:
                    task.status = TASK_STATUS_FAILED
                    db.merge(task)
                    db.commit()
                    log_task_history(db, task_type="file_cleanup", status="FAILED", details=str(e))
            except Exception as db_error:
                logger.error(f"Failed to update task status after failure: {db_error}")




@celery_app.task(name="app.tasks.tasks.send_reminder")
def send_reminder(task_id: int, receiver_email: str) -> None:
    """
    Send reminder email for a scheduled task.
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

            reminder_time = task.schedule_time
            if reminder_time:
                logger.info(
                    f"[Reminder] Task scheduled for {reminder_time} | Type: {task.task_type}"
                )
            else:
                logger.warning("Task has no schedule_time set.")

            # Send email reminder
            send_completion_email(task_id, receiver_email)
            logger.info(f"Sent reminder email to {receiver_email}")

            task.status = TASK_STATUS_COMPLETED
            db.commit()
            log_task_history(
                db,
                task_type="send_reminder",
                status="COMPLETED",
                details=f"Reminder email sent to {receiver_email}"
            )

    except Exception as e:
        logger.exception(f"Reminder task failed for ID {task_id}: {e}")
        if task:
            try:
                with SessionLocal() as db:
                    task.status = TASK_STATUS_FAILED
                    db.merge(task)
                    db.commit()
                    log_task_history(
                        db,
                        task_type="send_reminder",
                        status="FAILED",
                        details=str(e)
                    )
            except Exception as db_error:
                logger.error(f"Failed to update task status after reminder failure: {db_error}")


__all__ = ["shared_task", "send_reminder", "file_cleanup"]
