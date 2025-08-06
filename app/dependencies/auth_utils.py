from app.dependencies import OAuth2PasswordBearer,Depends, jwt, Session, HTTPException, get_db, status, SECRET_KEY, UserModel
from app.auth.auth import verify_token
from jwt import ExpiredSignatureError, InvalidTokenError
from app.utils.logger import SingletonLogger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
logger = SingletonLogger.get_logger()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Gets current user, using token and user in database """
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            logger.error("tried to get current_user, but no user was provided")
            raise InvalidTokenError("no sub proivided")
        
    except InvalidTokenError as e:
        logger.error(f"invalid token error {e}")
        raise InvalidTokenError("{e}")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        logger.error(f"no user found for user: {user_id}")
        raise InvalidTokenError(f"no user found nor token associated for {user_id}")
    return user
