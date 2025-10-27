"""
Utility functions for authentication and token verification.
Safe rewrite: import-friendly, avoids DB or logger issues at startup.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.auth import verify_token
from app.dependencies.constants import HTTP_STATUS_UNAUTHORIZED
from app.models.database import get_db
from app.models.user import UserModel
from app.utils.logger import SingletonLogger

# Only create objects that don't hit DB or filesystem at import time
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_logger():
    return SingletonLogger().get_logger()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Retrieve the current user based on a JWT token and DB lookup."""

    logger = get_logger()

    try:
        payload = verify_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            logger.error("Token missing 'sub' user ID")
            raise HTTPException(
                status_code=HTTP_STATUS_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            logger.warning("User not found in DB for ID %s", user_id)
            raise HTTPException(
                status_code=HTTP_STATUS_UNAUTHORIZED,
                detail="User not found or unauthorized",
            )

        return user

    except jwt.InvalidTokenError:
        logger.error("Invalid token format")
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="Invalid token",
        )


def admin_required(current_user: UserModel = Depends(get_current_user)):
    """Ensure user is admin before continuing."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
