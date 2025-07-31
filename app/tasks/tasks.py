"""CONTAINS ALL TASKS """

import os 
from app.models.tasks import TaskModel
from app.utils.celery_instance import celery_app
from app.utils.task import Session, get_db, datetime, timedelta



@celery_app.task
def file_cleanup(task_id: int):
    db: Session = get_db()
    try:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if task:
            task.status == "running"
            db.commit()

            threshold = datetime.now() - timedelta(days=7)
            for file in os.listdir("uploads"):
                filepath = os.path.join("uploads", file)
                if os.path.isfile(filepath) and datetime.fromtimestamp(os.path.getmtime(filepath) < threshold):
                    os.remove(filepath)
                    print(f"successfully delete{filepath}")
            task.status = "completed"
            db.commit()

    except Exception as e:
        task.status = "failed" if task else None
        db.commit()
        print(f"file cleanup failed for {task.id}")
    finally:
        db.close()
