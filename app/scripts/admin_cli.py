import argparse

from app.models.database import get_db
from app.models.user import UserModel
from app.models.tasks import Task


parser = argparse.ArgumentParser(description="Parser for admin tasks")
subparsers = parser.add_subparsers(dest="command", required=True)

# Subcommands
subparsers.add_parser('list-users', help="List all users")

delete_parser = subparsers.add_parser('delete-user', help="Delete user")
delete_parser.add_argument('user_id', type=int, help="User ID to delete")

subparsers.add_parser("view-tasks", help="List tasks")

cancel_parser = subparsers.add_parser('cancel-task', help="Cancel task using task_id")
cancel_parser.add_argument('task_id', type=int, help="ID of task to cancel")

args = parser.parse_args()

# Functions
def list_users():
    db = next(get_db())
    users = db.query(UserModel).all()
    if users:
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}")
    else:
        print("No users found.")

def delete_user(user_id):
    db = next(get_db())
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        print(f"User {user_id} deleted.")
    else:
        print(f"User {user_id} not found.")

def list_tasks():
    db = next(get_db())
    tasks = db.query(Task).all()
    if tasks:
        for task in tasks:
            print(f"Task {task.id}, Status: {task.status}, Description: {task.task_type}")
    else:
        print("No tasks to list.")

def delete_task(task_id):
    db = next(get_db())
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        print(f"Task {task_id} successfully deleted.")
    else:
        print(f"Task {task_id} not found.")

# Command Dispatcher
if args.command == 'list-users':
    list_users()

elif args.command == 'delete-user':
    delete_user(args.user_id)

elif args.command == 'view-tasks':
    list_tasks()

elif args.command == 'cancel-task':
    delete_task(args.task_id)
