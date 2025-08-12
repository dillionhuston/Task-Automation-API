"""Authentication router module for user registration and login."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models import UserModel
from app.schemas.user import User, UserCreate  # Adjust if needed
from app.models.database import get_db
from app.auth.auth import (
    hash_password,
    verify_password,
    jwt_generate
)
from app.dependencies.constants import HTTP_STATUS_UNAUTHORIZED
from app.utils.logger import SingletonLogger


router = APIRouter()
<<<<<<< Updated upstream
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
logger = SingletonLogger().get_logger()

=======
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
>>>>>>> Stashed changes

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user if email and username are unique."""
    db_user = db.query(UserModel).filter(
        (UserModel.email == user.email) | (UserModel.username == user.username)
    ).first()

    if db_user:
        logger.error("User already exists")
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Email or username already taken"
        )

    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        id=str(uuid.uuid4())
    )
    db.add(db_user)
    logger.info("New user added: %s", db_user.id)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
) -> dict:
    """Authenticate user and return a JWT access token."""
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.error("Invalid email or password provided in login")
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = jwt_generate({"sub": str(user.id)})
    logger.info("Token generated for user: %s", user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Returns the current user's token for validation."""
    return {"token": token}
