from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.user import UserModel
from app.models.tasks import Task
from app.dependencies.auth_utils import admin_required
from app.utils.logger import SingletonLogger

router = APIRouter(prefix="/admin", tags=["Admin"])
logger = SingletonLogger().get_logger()

# GET /admin/users
@router.get("/users")
def list_users(db: Session = Depends(get_db), admin: UserModel = Depends(admin_required)):
    if admin:
        users = db.query(UserModel).all()
        if not users:
            return {"message": "No users found."}
        return users
    else:
        logger.warn("user not admin")


# DELETE /admin/users/{user_id}
@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), admin: UserModel = Depends(admin_required)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted."}

# GET /admin/tasks
@router.get("/tasks")
def list_tasks(db: Session = Depends(get_db),admin: UserModel = Depends(admin_required)):
    tasks = db.query(Task).all()
    if not tasks:
        return {"message": "No tasks to list."}
    return tasks

# DELETE /admin/tasks/{task_id}
@router.delete("/tasks/{task_id}")
def cancel_task(task_id: int, db: Session = Depends(get_db), admin: UserModel = Depends(admin_required)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} successfully cancelled."}




@router.get("/summary")
def get_summary(db: Session = Depends(get_db), admin: UserModel = Depends(admin_required)):
    user_count = db.query(UserModel).count()
    task_count = db.query(Task).count()
    return {
        "total_users": user_count,
        "total_tasks": task_count,
    }
