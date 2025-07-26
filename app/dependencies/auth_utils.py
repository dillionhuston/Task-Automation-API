from app.dependencies import OAuth2PasswordBearer,Depends, jwt, Session, HTTPException, get_db, status, SECRET_KEY, UserModel
from app.auth.auth import verify_token

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
            raise credentials_exception
    except ValueError:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
