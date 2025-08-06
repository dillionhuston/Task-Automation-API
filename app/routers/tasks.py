from typing import List
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app.models.tasks import Task
from app.schemas.Tasks import TaskCreate, TaskResponse
from app.dependencies.auth_utils import get_current_user
from app.models.database import get_db
from app.utils.task import schedule_task
from app.utils.logger import SingletonLogger

from app.dependencies.constants import (
    ROUTE_SCHEDULE,
    ROUTE_LIST_TASKS,
    ROUTE_CANCEL_TASK,
    TASK_STATUS_CANCELLED,
    HTTP_STATUS_BAD_REQUEST,
)

router = APIRouter()
logger = SingletonLogger().get_logger()


@router.post(ROUTE_SCHEDULE, response_model=TaskResponse)
def schedule_logic(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> TaskResponse:
    try:
        new_task = schedule_task(
            db=db,
            user_id=user["id"],
            task_data=task,
            reciever_email=task.reciever_email
        )
        return TaskResponse.model_validate(new_task)
    except Exception as e:
        logger.exception(f"Error in scheduling task: {e}")
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="Invalid task"
        )


@router.get(ROUTE_LIST_TASKS, response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> List[TaskResponse]:
    tasks: List[Task] = db.query(Task).filter(Task.user_id == user["id"]).all()
    logger.debug("Tasks listed")
    return tasks


@router.get(ROUTE_CANCEL_TASK, response_model=TaskResponse)
def cancel_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
) -> TaskResponse:
    task: Task | None = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user["id"]
    ).first()

    if not task:
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="No matching task found or already completed"
        )

    task.status = TASK_STATUS_CANCELLED
    db.commit()
    db.refresh(task)
    return task
