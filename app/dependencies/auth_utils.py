from app.dependencies import OAuth2PasswordBearer,Depends, jwt, Session, HTTPException, get_db, status, SECRET_KEY, UserModel
from app.auth.auth import verify_token
from jwt import ExpiredSignatureError, InvalidSignatureError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise jwt.exceptions.InvalidTokenError
    except ValueError:
        raise jwt.exceptions.InvalidTokenError
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise jwt.exceptions.InvalidTokenError
    return user
