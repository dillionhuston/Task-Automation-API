from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.user import UserModel
from app.models.tasks import Task

router = APIRouter(prefix="/admin", tags=["Admin"])

# GET /admin/users
@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    if not users:
        return {"message": "No users found."}
    return users

# DELETE /admin/users/{user_id}
@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted."}

# GET /admin/tasks
@router.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    if not tasks:
        return {"message": "No tasks to list."}
    return tasks

# DELETE /admin/tasks/{task_id}
@router.delete("/tasks/{task_id}")
def cancel_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} successfully cancelled."}
