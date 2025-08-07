from app.routers import APIRouter, OAuth2PasswordBearer, User, Depends, UserModel
from app.routers import User, Session, get_db, HTTPException, hash_password, uuid, status, Annotated, OAuth2PasswordRequestForm, verify_password, jwt_generate, UserCreate, APIRouter
from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    HTTP_STATUS_BAD_REQUEST, 
    HTTP_STATUS_UNAUTHORIZED
)

# use this for oauth2 password only, without client-id or token 
"""class PasswordOnlyOAuth2(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)"""


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
logger = SingletonLogger().get_logger()

@router.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db))->None:
    """Checks if user exists, if not then we can go ahead and register user to database"""
    db_user = db.query(UserModel).filter(
        (UserModel.email == user.email) | (UserModel.username == user.username)).first()
    
    #if user exists in datbase
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
    logger.info(f"new user added {db_user.id}")

    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)])->None:

    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.error("Invalid email or password provided in login")

        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = jwt_generate({"sub": str(user.id)})
    logger.info(f"token egenrated for {user.id}")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(token: str = Depends(oauth2_scheme)):# noqa: 
    """Gets current user"""
    return {"token": token}