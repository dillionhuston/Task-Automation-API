import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.schemas.User import User, UserCreate
from app.models.database import get_db
from app.auth.auth import hash_password, verify_password, jwt_generate
from app.dependencies.constants import HTTP_STATUS_UNAUTHORIZED
from app.utils.logger import SingletonLogger

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
logger = SingletonLogger().get_logger()


@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = db.query(UserModel).filter(
        (UserModel.email == user.email) | (UserModel.username == user.username)
    ).first()

    if db_user:
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Email or username already taken"
        )

    db_user = UserModel(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_admin=user.is_admin
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = jwt_generate({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
