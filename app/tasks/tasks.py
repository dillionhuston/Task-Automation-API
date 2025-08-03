import os
from app.models.tasks import Task
from app.utils.celery_instance import celery_app
from app.models.database import SessionLocal  
from datetime import datetime, timedelta
from celery import shared_task
from app.utils.email import schedule_reminder, send_completion_email


@celery_app.task(name="app.tasks.tasks.file_cleanup")
def file_cleanup(task_id: int):
    task = None
    try:
        with SessionLocal() as db:  
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "running" # removed "=="
                db.commit()

                threshold = datetime.now() - timedelta(days=1)
                uploads_dir = "uploads"
                for file in os.listdir(uploads_dir):
                    filepath = os.path.join(uploads_dir, file)
                    # fixed parenthes
                    if os.path.isfile(filepath) and datetime.fromtimestamp(os.path.getmtime(filepath)) < threshold:
                        os.remove(filepath)
                        print(f"Successfully deleted {filepath}")

                task.status = "completed"
                db.commit()
                send_completion_email(task_id,receiver_email="d9392828@gmail.com")
            else:
                print(f"No task found with id {task_id}")

    except Exception as e:
        print(f"File cleanup failed for task {task_id}: {e}")
        if task:
            with SessionLocal() as db:
                task.status = "failed"
                db.merge(task)
                db.commit()
        else:
            print("No task object to update status")




@celery_app.task(name="app.tasks.task.send_reminder")  
def send_reminder(task_id: int):
    task = None
    try:
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if not task:
                print(f"No task found with ID {task_id}")
                return
            task.status = "scheduled"
            schedule_reminder(task_id, receiver_email="d9392828@gmail.com")
            db.commit()

            reminder_time = task.schedule_time
            if reminder_time:
                print(f"[Reminder] Task scheduled for {reminder_time} | Type: {task.task_type}")
            else:
                print("Task has no schedule_time set.")

            task.status = "completed"
            db.commit()

    except Exception as e:
        print(f"Reminder task failed for ID {task_id}: {e}")
        if task:
            with SessionLocal() as db:
                task.status = "failed"
                db.merge(task)
                db.commit()