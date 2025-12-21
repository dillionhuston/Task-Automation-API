"""
Task management routes for Task Automation API.
Includes scheduling, listing, cancelling, and deleting tasks.
Fully compatible with UUID task IDs and your current auth system.
"""

from typing import Optional

from uuid import UUID
from typing import List
from fastapi import APIRouter, Form, Depends, HTTPException, Path, File, UploadFile
from sqlalchemy.orm import Session

from app.models.tasks import Task, TaskHistory
from app.schemas.tasks import TaskCreate, TaskResponse, TaskHistoryS
from app.dependencies.auth_utils import get_current_user
from app.models.database import get_db
from app.utils.task import schedule_task
from app.utils.logger import SingletonLogger
from app.models.user import UserModel
from app.dependencies.constants import HTTP_STATUS_BAD_REQUEST

from app.schemas.tasks import TaskType
from datetime import datetime

router = APIRouter(prefix="/tasks")
logger = SingletonLogger().get_logger()


@router.post("/schedule", response_model=TaskResponse)
# sorry this is probaly the only way we can add a file as optional. I cant use a schema to combine them both
async def schedule_task_endpoint(
    title: str = Form(...),
    description: str = Form(...),
    receiver_email: str = Form(...),
    task_type: TaskType = Form(...),
    schedule_time: datetime = Form(...),
    webhook_url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    try:
        task_data = TaskCreate(
            title=title,
            description=description,
            receiver_email=receiver_email,
            task_type=task_type,
            schedule_time=schedule_time,
            webhook_url=webhook_url
        )

       
        # Schedule the task (file is optional)
        new_task = await schedule_task(
            db=db,
            user_id=str(user.id),
            task_data=task_data,
            receiver_email=receiver_email,
            webhook_url=webhook_url,
            file=file
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
    try:
        tasks = db.query(TaskHistory).filter(TaskHistory.user_id == str(user.id)).all()
        task_history = []
        for task in tasks:  #
            task_history.append({
                "id": str(task.id),
                "schedule_time": task.executed_at,
                "status": task.status,
                "task_type": task.task_type,
                "details": task.details,
                "user_id": task.user_id,
                "executed_at": task.executed_at
            })

        return task_history
            
    except Exception as exc:
        logger.error("Error querying tasks for user %s: %s", user.id, str(exc))
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="Error retrieving tasks"
        ) from exc

def validate_uuid(task_id: str) -> UUID:
    try:
        return UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID format. Must be a valid UUID (e.g. a932dab1-5cb1-485c-8ccc-b3b48dc1c4c0)"
        )


@router.post("/cancel_task/{task_id}", response_model=TaskResponse)
async def cancel_task_endpoint(
    task_id: str = Path(..., description="Task UUID"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    validate_uuid(task_id)

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == str(user.id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or doesn't belong to you")

    if task.cancelled:
        raise HTTPException(status_code=400, detail="Task is already cancelled")

    task.cancelled = True
    db.commit()
    db.refresh(task)

    logger.info("Task %s cancelled by user %s", task_id, user.id)
    return TaskResponse.model_validate(task)


@router.delete("/delete_task/{task_id}", response_model=TaskResponse)
async def delete_task_endpoint(
    task_id: str = Path(..., description="Task UUID to permanently delete"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    validate_uuid(task_id)

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == str(user.id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or already deleted")

    db.delete(task)
    db.commit()

    logger.info("Task %s permanently deleted by user %s", task_id, user.id)
    return TaskResponse.model_validate(task)


@router.get("/task_history", response_model=List[TaskHistoryS])
async def task_History(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)
):
    history = db.query(TaskHistory).filter(TaskHistory.user_id == str(user.id)).order_by(TaskHistory.executed_at.desc()).all()
    
    return [TaskHistoryS.model_validate(task) for task in history]

