#make routers a subpackage of app


from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.oauth2 import OAuth2
from sqlalchemy.orm import Session
from typing import Annotated
import uuid
from app.schemas.User import UserCreate, User  
from app.models.user import UserModel  
from app.models.database import get_db
from app.auth.auth import hash_password, verify_password, jwt_generate
from app.dependencies.auth_utils import get_current_user
