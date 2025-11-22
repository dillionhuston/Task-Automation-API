"""
Admin routes for Task Automation API.
Includes user and task management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.user import UserModel
from models.tasks import Task
from dependencies.auth_utils import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", dependencies=[Depends(admin_required)])
def list_users(db: Session = Depends(get_db)):
    """Return a list of all registered users (admin only)."""
    users = db.query(UserModel).all()
    if not users:
        return {"message": "No users found."}
    return users


@router.delete("/users/{user_id}", dependencies=[Depends(admin_required)])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user by ID (admin only)."""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted."}


@router.get("/tasks", dependencies=[Depends(admin_required)])
def list_tasks(db: Session = Depends(get_db)):
    """List all tasks (admin only)."""
    tasks = db.query(Task).all()
    if not tasks:
        return {"message": "No tasks to list."}
    return tasks


@router.delete("/tasks/{task_id}", dependencies=[Depends(admin_required)])
def cancel_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID (admin only)."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} successfully cancelled."}


@router.get("/summary", dependencies=[Depends(admin_required)])
def get_summary(db: Session = Depends(get_db)):
    """Return total users and tasks count (admin only)."""
    user_count = db.query(UserModel).count()
    task_count = db.query(Task).count()
    return {"total_users": user_count, "total_tasks": task_count}
