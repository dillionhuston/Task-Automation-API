"""
Task management endpoints for scheduling, listing, and canceling tasks.
"""

from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.models.tasks import Task
from app.schemas.Tasks import TaskCreate, TaskResponse
from app.dependencies.auth_utils import get_current_user
from app.models.database import get_db
from app.utils.task import schedule_task
from app.utils.logger import SingletonLogger

from app.dependencies.constants import (
    TASK_STATUS_CANCELLED,
    HTTP_STATUS_BAD_REQUEST,
)

router = APIRouter()
logger = SingletonLogger().get_logger()


@router.post('/schedule', response_model=TaskResponse)
def schedule_logic(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> TaskResponse:
    """
    Schedule a new task for the authenticated user.
    """
    try:
        new_task = schedule_task(
            db=db,
            user_id=user["id"],
            task_data=task,
            receiver_email=task.receiver_email  # fixed spelling here
        )
        new_task = schedule_task(db=db, user_id=user.id, task_data=task, reciever_email=task.reciever_email)
        return TaskResponse.model_validate(new_task)

    except Exception as e:
        logger.exception("Error in scheduling task: %s", e)
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="Invalid task, failed to validate or wrong details"
        ) from e


@router.get('/list_tasks', response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> List[TaskResponse]:
    """
    List all tasks for the authenticated user.
    """
    tasks: List[Task] = db.query(Task).filter(Task.user_id == user["id"]).all()
    logger.debug("Tasks listed for user %s", user["id"])
    return tasks


@router.get('cancel_task{task_id}', response_model=TaskResponse)
def cancel_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> TaskResponse:
    """
    Cancel a task by task_id if it belongs to the user.
    """
    task: Task | None = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user["id"]
    ).first()

    if not task:
        logger.error("No matching task found for task_id %s and user %s", task_id, user["id"])
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail=f"No matching task found with ID {task_id} or task already completed"
        )

    task.status = TASK_STATUS_CANCELLED
    db.commit()
    db.refresh(task)
    logger.info("Task %s cancelled for user %s", task_id, user["id"])
    return task
