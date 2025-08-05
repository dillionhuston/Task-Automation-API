from typing import List
from app.routers import get_current_user, get_db, Depends, Task, User, Session, Annotated, HTTPException, status, APIRouter, TaskCreate
from app.schemas.Tasks import TaskCreate, TaskResponse, TaskStatus, TaskType
from app.utils.task import schedule_task
from app.utils.logger import logger

router = APIRouter()


@router.post("/schedule", response_model=TaskResponse)
def schedule_logic(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)) -> TaskResponse:
    try:
        new_task = schedule_task(db=db, user_id=user["id"], task_data=task, reciever_email=task.reciever_email)
        return TaskResponse.model_validate(new_task)
    except Exception as e:
        logger.exception("error in scheduling task {e}")
        raise status.HTTP_404_NOT_FOUND("{e}")


@router.get("/list_tasks", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)) -> List[TaskResponse]:
    tasks: List[Task] = db.query(Task).filter(Task.user_id == user["id"]).all()
    logger.debug("files listed")
    return tasks


@router.get("/cancel/{task_id}", response_model=TaskResponse)
def cancel_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)) -> TaskResponse:
    
    task: Task | None = db.query(Task).filter(Task.id == task_id, Task.user_id == user["id"]).first()
    if not task:
        raise status.HTTP_400_BAD_REQUEST
    task.status = TaskStatus.canceled
    db.commit()
    db.refresh(task)
    return task
