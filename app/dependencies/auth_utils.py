"""Utility functions for authentication and token verification."""
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.auth import verify_token
from app.dependencies.constants import HTTP_STATUS_UNAUTHORIZED
from app.models.database import get_db
from app.models.user import UserModel
from app.utils.logger import SingletonLogger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
logger = SingletonLogger().get_logger()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Retrieve the current user based on a JWT token and DB lookup."""
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            logger.exception("Attempted to get current user, but no user ID provided in token.")
            raise HTTPException(
                status_code=HTTP_STATUS_UNAUTHORIZED,
                detail="No user_id provided in token"
            )

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            logger.warning("No user found in database for user ID: %s", user_id)
            raise HTTPException(
                status_code=HTTP_STATUS_UNAUTHORIZED,
                detail=f"Cannot find user in database with user_id: {user_id}"
            )
        return user

    except jwt.InvalidTokenError as e: # pylint: disable=no-member
        logger.exception("Token verification failed")
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Token verification failed"
        ) from e




def admin_required(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user