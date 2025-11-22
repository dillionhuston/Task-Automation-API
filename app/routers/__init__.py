"""
Make routers a subpackage of app.
"""

from app.routers.auth import register, read_current_user
from app.routers.files import upload_file, list_files, delete_file
# from .tasks import schedule_task_endpoint, list_tasks_endpoint, cancel_task_endpoint

__all__ = [
    "register",
    "read_current_user",
    "upload_file",
    "list_files",
    "delete_file",
    # "schedule_task_endpoint",
    # "list_tasks_endpoint",
    # "cancel_task_endpoint",
]
