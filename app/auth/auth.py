"""Authentication module for JWT token creation, verification, and password hashing."""

from fastapi import HTTPException
import jwt
from ..auth import SECRET_KEY, pbkdf2_sha256
from ..dependencies.constants import HTTP_STATUS_UNAUTHORIZED
from ..utils.logger import SingletonLogger
logger = SingletonLogger().get_logger()
def hash_password(password: str) -> str:
    """Hash a password using pbkdf2_sha256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash using pbkdf2_sha256.

    Args:
        password (str): The password to verify.
        password_hash (str): The hashed password from the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pbkdf2_sha256.verify(password, password_hash)

def jwt_generate(payload: dict[str, int]) -> str:
    """Generate a JWT token using user ID.

    Args:
        payload (dict[str, int]): Payload containing user ID.

    Returns:
        str: Encoded JWT token.
    """
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256") # pylint: disable=no-member
    logger.info("Token generated for user ID: %s", payload.get("user_id"))
    return token

def verify_token(token: str) -> dict:
    """Verify a JWT token and return its decoded payload.

    Args:
        token (str): The JWT token from OAuth2 bearer.

    Returns:
        dict: Decoded token payload.

    Raises:
        HTTPException: If the token is expired or invalid.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # pylint: disable=no-member
    except jwt.ExpiredSignatureError as exc:  # pylint: disable=no-member
        logger.exception("Token has expired")
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="token has expired"
        ) from exc
    except jwt.InvalidTokenError as exc:  # pylint: disable=no-member
        logger.exception("Invalid token provided")
        raise HTTPException(
            status_code=HTTP_STATUS_UNAUTHORIZED,
            detail="invalid token"
        ) from exc
