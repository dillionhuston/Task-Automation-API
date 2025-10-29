"""
Module for handling email notifications with Celery tasks.
Includes reminder and completion email functionality.
"""

import smtplib
import ssl
import os
from email.message import EmailMessage

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.utils.celery_instance import celery_app
from app.models.database import SessionLocal
from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    TASK_STATUS_SCHEDULED,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_FAILED,
)

logger = SingletonLogger().get_logger()

# Load and check environment variables
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('PASSWORD')
SMTP_PORT = 465
SMTP_SERVER = "smtp.gmail.com"

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    logger.critical("EMAIL or PASSWORD environment variable is missing")
    raise ValueError("Missing EMAIL or PASSWORD in .env file")


@celery_app.task(name="app.utils.email.send_email_task", bind=True, autoretry_for=(smtplib.SMTPException,), retry_backoff=True, max_retries=3)
def send_email_task(self, receiver_email: str, task_id: int, email_type: str):
    from app.models.tasks import Task
    db: Session = SessionLocal()
    task: Task | None = None

    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.error("Task %d not found", task_id)
            return "Task Not Found"

        if not receiver_email:
            logger.warning("Task %d has no receiver email", task_id)
            task.status = TASK_STATUS_FAILED
            db.merge(task)
            db.commit()
            return "No Email Provided"

        # Build email
        subject = f"Task '{task.title}' Completed" if email_type == TASK_STATUS_COMPLETED else f"Reminder: Task '{task.title}' Due"
        body = f"Task ID: {task.id}\nTitle: {task.title}\nStatus: {task.status}\nScheduled: {task.schedule_time}"

        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        logger.info("Email sent to %s for task %d", receiver_email, task_id)

        # Update task status
        task.status = TASK_STATUS_COMPLETED
        db.merge(task)
        db.commit()
        return "Success"

    except smtplib.SMTPException as smtp_err:
        logger.error("SMTP error: %s", smtp_err)
        if task:
            task.status = TASK_STATUS_FAILED
            db.merge(task)
            db.commit()
        raise self.retry(exc=smtp_err)

    except Exception as exc:
        logger.exception("Unhandled error: %s", exc)
        if task:
            task.status = TASK_STATUS_FAILED
            db.merge(task)
            db.commit()
        raise

    finally:
        db.close()

def schedule_reminder(task_id: int, receiver_email: str):
    """Schedule an email reminder for the specified task."""
    send_email_task.delay(receiver_email, task_id, email_type=TASK_STATUS_SCHEDULED)


def send_completion_email(task_id: int, receiver_email: str):
    """Send a completion notification email for the specified task."""
    send_email_task.delay(receiver_email, task_id, email_type=TASK_STATUS_COMPLETED)
