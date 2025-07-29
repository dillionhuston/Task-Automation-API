import hashlib
import os 
from app.models import UserModel
from app.models.database import get_db
from app.dependencies import verify_token
from fastapi import HTTPException, UploadFile
from datetime import datetime
from celery import Celery
