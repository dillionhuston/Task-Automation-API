from app.routers import get_current_user, get_db, Depends, Task, User, Session, Annotated, HTTPException, status, APIRouter, TaskCreate
from app.schemas.Tasks import TaskCreate, TaskResponse, TaskStatus, TaskType
from app.utils.task import schedule_task
from app.schemas.Tasks import TaskResponse
router = APIRouter()



# schedule a task 
@router.post("/schedule")
def schedule_logic(
        task: TaskCreate,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    try:
        new_task = schedule_task(db=db, user_id=user.id, task_data=task)
        return TaskResponse.model_validate(new_task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




#list tasks for user 
@router.get("/list_tasks", response_model= list[TaskResponse])
def list_tasks(
     db: Session = Depends(get_db), 
     user: dict = Depends(get_current_user)
):
     tasks = db.query(Task).filter(Task.user_id == user['id']).all()
     return tasks



#cancel a task linked to user 
@router.get("/cancel/{task_id}", response_model=TaskResponse)
def cancel_task(
     task_id: int,
     db: Session = Depends(get_db),
     user: dict = Depends(get_current_user)
):
     task = db.query(Task).filter(Task.id == task_id, Task.user_id == user['id']).first()
     if not task:
          raise HTTPException(status_code=400, detail="task doesnt exist or cant be found")
     task.status = "cancelled"
     db.commit()
     db.refresh(task)
     return task


