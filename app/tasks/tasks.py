"""
Celery tasks for handling scheduled jobs such as file cleanup and sending reminders.
"""

import os
from typing import Optional
from datetime import datetime, timedelta
from celery import shared_task

from app.models.tasks import Task
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

# need to execute on client machine not server
# reverting this to poll server
def file_cleanup(task_id: int, receiver_email: str | None) -> None:
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
                if os.path.isfile(filepath) and \
                   datetime.fromtimestamp(os.path.getmtime(filepath)) < threshold:
                    os.remove(filepath)
                    deleted_count += 1

            logger.info(f"Deleted {deleted_count} old files.")

            task.status = TASK_STATUS_COMPLETED
            db.commit()

            if receiver_email:
                send_completion_email(task_id, receiver_email)
                logger.info(f"Sent task completion email to {receiver_email}")
            else:
                logger.warning(f"Task {task_id} has no receiver_email. No email sent.")

    except Exception as e:
        logger.exception(f"File cleanup failed for task_id={task_id}: {e}")

        if task:
            try:
                with SessionLocal() as db:
                    task.status = TASK_STATUS_FAILED
                    db.merge(task)
                    db.commit()
            except Exception as db_error:
                logger.error(f"Failed to update task status after failure: {db_error}")




@celery_app.task(name="app.tasks.tasks.send_reminder")
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

            task.status = TASK_STATUS_RUNNING
            db.commit()


            reminder_time = task.schedule_time
            if reminder_time:
                logger.info(
                    f"[Reminder] Task scheduled for {reminder_time} "
                    f"| Type: {task.task_type}"
                )
            else:
                logger.warning("Task has no schedule_time set.")

            task.status = TASK_STATUS_COMPLETED
            db.commit()

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.exception(f"Reminder task failed for ID {task_id}: {e}")
        if task:
            try:
                with SessionLocal() as db:
                    task.status = TASK_STATUS_FAILED
                    db.merge(task)
                    db.commit()
            except Exception as db_error:  # pylint: disable=broad-exception-caught
                logger.error(f"Failed to update task status after reminder failure: {db_error}")


__all__ = ["shared_task", "send_reminder", "file_cleanup"]
