"""
Contains only the task scheduling function.
"""

from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.tasks import Task
from app.schemas.Tasks import TaskCreate, TaskStatus, TaskResponse
from app.utils.celery_instance import celery_app
from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    TASK_TYPE_FILE_CLEANUP,
    TASK_TYPE_REMINDER,
    TASK_ID_GENERATOR,
)

logger = SingletonLogger().get_logger()

def schedule_task(db, user_id: str, task_data, receiver_email: str):
    new_task = Task(
        id=str(uuid4()),                 
        user_id=str(user_id),             
        task_type=task_data.task_type.value,  
        schedule_time=task_data.schedule_time,
        status=TaskStatus.scheduled.value,    
        receiver_email=receiver_email,
        title=task_data.title
    )


    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(
        "New task scheduled: %s (ID: %s) for user %s at %s",
        new_task.task_type,
        new_task.id,
        new_task.user_id,
        new_task.schedule_time,
        new_task.receiver_email
    )


    ## take this part out. need to poll sevrer
    ###if task_data.task_type == TASK_TYPE_FILE_CLEANUP:
       ### poll_server()###

        
    if task_data.task_type == TASK_TYPE_REMINDER:
        celery_app.send_task(
            name="app.tasks.tasks.send_reminder",
            args=[str(new_task.id), receiver_email],
            eta=new_task.schedule_time,
        )

    return TaskResponse.model_validate(new_task)
