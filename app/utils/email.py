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
    TASK_STATUS_CANCELLED, 
    TASK_TYPE_REMINDER,
    TASK_STATUS_COMPLETED)

logger = SingletonLogger.get_logger()
load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('PASSWORD')
SMTP_PORT = 465
SMTP_SERVER = "smtp.gmail.com"

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    logger.exception("no email/password in .env")
    raise ValueError("EMAIL or PASSWORD environment variable is missing")

@celery_app.task(name="app.utils.email.")
def send_email_task(receiver_email: str, task_id: int, email_type: str):
    db: Session = SessionLocal()
    try:
        from app.models.tasks import Task  
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.error(f"Task with ID {task_id} not found")
            return
        TASK_TYPE_REMINDER = TaskStatus.scheduled
        TASK_STATUS_COMPLETED = TaskStatus.completed
        
        msg = EmailMessage()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['Subject'] = (
        f"Reminder: Task '{task.title}' Due Soon"
        if TASK_TYPE_REMINDER
        else  f"Task '{task.title}' completed"
)
        body = (
            f"Dear User,\n\n"
            f"This is a {'reminder' if email_type == 'reminder' else 'completion'} for task '{task.title}'.\n"
            f"Details:\n"
            f"- Task ID: {task.id}\n"
            f"- Due Date: {task.schedule_time}\n"
            f"- Status: {task.status}\n\n"
            f"{'Please complete the task by the due date.' if email_type == 'reminder' else 'Congratulations on completing the task!'}"
        )
        msg.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            try:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                logger.info(f"server logged in {EMAIL_ADDRESS}")
                server.send_message(msg)
                logger.info(f"Email sent to {receiver_email} for task {task_id} ({email_type})")
            except smtplib.SMTPException as e:
                logger.error(f"Failed to send email to {receiver_email}: {str(e)}")
                raise

    except Exception as e:
        logger.error(f"Error in send_email_task: {str(e)}")
        raise
    finally:
        db.close()

def schedule_reminder(task_id: int, receiver_email: str):
    send_email_task.delay(receiver_email, task_id, email_type=TASK_STATUS_SCHEDULED)

def send_completion_email(task_id: int, receiver_email: str):
    send_email_task.delay(receiver_email, task_id, email_type=TASK_STATUS_COMPLETED)