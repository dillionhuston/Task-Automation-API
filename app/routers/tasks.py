from app.routers import get_current_user, get_db, Depends, TaskModel, User, Session, Annotated, HTTPException, status, APIRouter, TaskCreate
from app.schemas.Tasks import TaskCreate, TaskResponse, TaskStatus, TaskType
from app.utils.task import schedule_task
router = APIRouter()


router.post("/schedule")
def schedule_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user)
):
    try:
         new_task = schedule_task(db=db, user_id=user['id'], task_data=task)
         return new_task
    except Exception as e:
         raise HTTPException(status_code=400, detail={e})    

    


