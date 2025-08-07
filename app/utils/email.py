import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from app.utils.celery_instance import celery_app
from app.models.database import SessionLocal
from app.schemas.Tasks import TaskStatus
from sqlalchemy.orm import Session
from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    TASK_STATUS_SCHEDULED,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_FAILED,
    TASK_TYPE_REMINDER
)

logger = SingletonLogger().get_logger()

# Load and check environment
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('PASSWORD')
SMTP_PORT = 465
SMTP_SERVER = "smtp.gmail.com"

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    logger.critical("EMAIL or PASSWORD environment variable is missing")
    raise ValueError("Missing EMAIL or PASSWORD in .env file")

@celery_app.task(name="app.utils.email.send_email_task")
def send_email_task(receiver_email: str, task_id: int, email_type: str):
    """
    Celery task to send reminder or completion emails.
    """
    db: Session = SessionLocal()
    try:
        from app.models.tasks import Task  # local import to avoid circular deps
        task = db.query(Task).filter(Task.id == task_id).first()

        if not task:
            logger.error(f"Task with ID {task_id} not found")
            return

        db.commit()

        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = (
            f"Reminder: Task '{task.title}' Due Soon"
            if email_type == TASK_STATUS_SCHEDULED
            else f"Task '{task.title}' Completed"
        )

        body = (
            f"Dear User,\n\n"
            f"This is a {'reminder' if email_type == TASK_STATUS_SCHEDULED else 'confirmation'} for your task '{task.title}'.\n"
            f"- Task ID: {task.id}\n"
            f"- Due Date: {task.schedule_time}\n"
            f"- Status: {task.status}\n\n"
            f"{'Please complete the task by the due date.' if email_type == TASK_STATUS_SCHEDULED else 'Congratulations on completing your task!'}"
        )
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            logger.info(f"Email sent to {receiver_email} for task {task_id} ({email_type})")

    except smtplib.SMTPException as smtp_err:
        logger.error(f"SMTP error while sending email to {receiver_email}: {smtp_err}")
        if task:
            task.status = TASK_STATUS_FAILED
            db.commit()
        raise

    except Exception as e:
        logger.exception(f"Unhandled error in send_email_task: {e}")
        if task:
            task.status = TASK_STATUS_FAILED
            db.commit()
        raise

    finally:
        db.close()

def schedule_reminder(task_id: int, receiver_email: str):
    send_email_task.delay(receiver_email, task_id, email_type=TASK_STATUS_SCHEDULED)

def send_completion_email(task_id: int, receiver_email: str):
    send_email_task.delay(receiver_email, task_id, email_type=TASK_STATUS_COMPLETED)
