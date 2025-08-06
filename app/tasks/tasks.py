import os
from typing import Optional
from app.models.tasks import Task
from app.utils.celery_instance import celery_app
from app.models.database import SessionLocal  
from app.schemas.Tasks import TaskStatus
from datetime import datetime, timedelta
from celery import shared_task
from app.utils.email import schedule_reminder, send_completion_email
from app.utils.logger import SingletonLogger 

logger = SingletonLogger.get_logger()


@celery_app.task(name="app.tasks.tasks.file_cleanup")
def file_cleanup(task_id: int, reciever_email: str) -> None:
    """
    Celery task to delete files older than one day from the uploads directory.
    Args:
        task_id (int): The ID of the task to update status for.
        reciever_email (str): Email address to notify upon completion.
    Returns:
        None
    Side effects:
        Deletes old files, updates task status, sends completion email.
    """
    task: Optional[Task] = None # set as none as task be "none" at first
    try:
        with SessionLocal() as db:  
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = TaskStatus.running 
                db.commit()

                threshold: datetime = datetime.now() - timedelta(days=1)
                uploads_dir: str = "uploads"
                for file in os.listdir(uploads_dir):
                    filepath: str = os.path.join(uploads_dir, file)
                    if os.path.isfile(filepath) and datetime.fromtimestamp(os.path.getmtime(filepath)) < threshold:
                        os.remove(filepath)
                        print(f"Successfully deleted {filepath}")

                task.status = TaskStatus.completed
                db.commit()
                send_completion_email(task_id, reciever_email)
            else:
                print(f"No task found with id {task_id}")

    except Exception as e:
        print(f"File cleanup failed for task {task_id}: {e}")
        if task:
            with SessionLocal() as db:
                task.status = TaskStatus.failed
                db.merge(task)
                db.commit()
        else:
            print("No task object to update status")


@celery_app.task(name="app.tasks.task.send_reminder")  
def send_reminder(task_id: int, receiver_email: str) -> None:
    """
    Celery task to send an email reminder for a scheduled task.
    Args:
        task_id (int): The ID of the task to send a reminder for.
        receiver_email (str): Email address to send the reminder to.
    Returns:
        None
    Side effects:
        Sends reminder email, updates task status, logs info or errors.
    """
    task: Optional[Task] = None
    try:
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                print(f"No task found with ID {task_id}")
                return
            task.status = TaskStatus.scheduled
            schedule_reminder(task_id, receiver_email)
            db.commit()

            reminder_time: Optional[datetime] = task.schedule_time
            if reminder_time:
                print(f"[Reminder] Task scheduled for {reminder_time} | Type: {task.task_type}")
            else:
                print("Task has no schedule_time set.")

            task.status = TaskStatus.completed
            db.commit()

    except Exception as e:
        print(f"Reminder task failed for ID {task_id}: {e}")
        if task:
            with SessionLocal() as db:
                task.status = TaskStatus.failed
                db.merge(task)
                db.commit()


__all__ = ["shared_task", "send_reminder"]
