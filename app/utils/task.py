"""
Contains only the task scheduling function.
"""

import uuid
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


def schedule_task(db: Session, user_id: str, task_data: TaskCreate, receiver_email: str) -> TaskResponse:
    """
    Schedule a new Celery task based on type and time.

    Args:
        db (Session): Active database session.
        user_id (str): User's UUID.
        task_data (TaskCreate): Incoming task data.
        receiver_email (str): Email to notify after task.

    Returns:
        TaskResponse: The scheduled task, validated as response model.
    """
    new_task = Task(
        id=TASK_ID_GENERATOR,
        user_id=uuid.UUID(user_id),
        task_type=task_data.task_type,
        schedule_time=task_data.schedule_time,
        status=TaskStatus.scheduled,
        title=task_data.title,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(
        "New task scheduled: %s (ID: %s) for user %s at %s",
        new_task.task_type,
        new_task.id,
        new_task.user_id,
        new_task.schedule_time,
    )

    if task_data.task_type == TASK_TYPE_FILE_CLEANUP:
        celery_app.send_task(
            name="app.tasks.tasks.file_cleanup",
            args=[str(new_task.id), receiver_email],
            eta=new_task.schedule_time,
        )

    elif task_data.task_type == TASK_TYPE_REMINDER:
        celery_app.send_task(
            name="app.tasks.tasks.send_reminder",
            args=[str(new_task.id), receiver_email],
            eta=new_task.schedule_time,
        )

    return TaskResponse.model_validate(new_task)
