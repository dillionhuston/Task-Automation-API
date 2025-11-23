"""
Task management routes for Task Automation API.
Includes scheduling, listing, and cancelling tasks for the current user.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.tasks import Task
from ..schemas.tasks import TaskCreate, TaskResponse
from ..dependencies.auth_utils import get_current_user
from ..models.database import get_db
from ..utils.task import schedule_task
from ..utils.logger import SingletonLogger
from ..models.user import UserModel
from ..dependencies.constants import TASK_STATUS_CANCELLED, HTTP_STATUS_BAD_REQUEST
from ..tasks.tasks import celery_app

router = APIRouter()
logger = SingletonLogger().get_logger()


@router.post("/schedule", response_model=TaskResponse)
def schedule_task_endpoint(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    """
    Schedule a new task for the current user.

    Raises:
        HTTPException: If task validation fails.
    """
    try:
        new_task = schedule_task(
            db=db,
            user_id=str(user.id),
            task_data=task,
            receiver_email=task.receiver_email
        )
        return new_task
    except Exception as e:
        logger.exception("Error scheduling task: %s", e)
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="Invalid task, failed to validate or wrong details"
        ) from e


@router.get("/list_tasks", response_model=List[TaskResponse])
def list_tasks_endpoint(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    """
    List all tasks for the current user.
    """
    tasks = db.query(Task).filter(Task.user_id == str(user.id)).all()
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/cancel_task/{task_id}", response_model=TaskResponse)
def cancel_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    """
    Cancel a task for the current user by setting its status to cancelled.

    Raises:
        HTTPException: If no matching task is found.
    """
    task: Task | None = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == str(user.id)
    ).first()

    if not task:
        logger.error(
            "No matching task found for task_id %s and user %s",
            task_id, user.id
        )
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail=f"No matching task found with ID {task_id} or task already completed"
        )

    task.status = TASK_STATUS_CANCELLED
    db.commit()
    db.refresh(task)
    logger.info("Task %s cancelled for user %s", task_id, user.id)
    return task
