"""Make routers a subpackage of app."""

import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.oauth2 import OAuth2
from sqlalchemy.orm import Session

from app.schemas.User import UserCreate, User
from app.schemas.File import File as FileSchema
from app.schemas.Tasks import TaskCreate

from app.models.user import UserModel
from app.models.file import FileModel
from app.models.tasks import Task
from app.models.database import get_db

from app.auth.auth import hash_password, verify_password, jwt_generate
from app.dependencies.auth_utils import get_current_user
from app.utils.file import compute, save_file

from .auth import register, read_current_user
from .files import upload_file, list_files, delete_file
from .tasks import schedule_logic, list_tasks, cancel_task

__all__ = [
    "register",
    "read_current_user",
    "upload_file",
    "list_files",
    "delete_file",
    "schedule_logic",
    "list_tasks",
    "cancel_task",
]
