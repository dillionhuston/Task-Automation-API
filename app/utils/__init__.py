"""
Utility functions and helpers for the app.
"""

import hashlib
import os
from datetime import datetime

from fastapi import HTTPException, UploadFile
from celery import Celery

from app.models import UserModel
from app.models.database import get_db
