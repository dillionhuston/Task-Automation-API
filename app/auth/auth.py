"""Contains user auth and jwt generation"""
from app.auth import jwt, os, pbkdf2_sha256, load_dotenv
from app.auth import SECRET_KEY
from app.utils.logger import SingletonLogger


logger = SingletonLogger.get_logger()

def hash_password(password: str)->None:
    return pbkdf2_sha256.hash(password)

def verify_password(password, password_hash: str) -> bool:
    """Verify usser password with sha256
    Args: Password str, database_password_hash
    """
    return pbkdf2_sha256.verify(password, password_hash)

def jwt_generate(payload: dict[str, int])->str:
    """Generate JWT token, using user id
    Args: payload(dict)
    """
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    logger.info(f"token generated for new user {payload.get('user_id')}")
    return token


def verify_token(token: str) -> dict:
    """Verify user jwt token
    Args: token from oauth2 bearer
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256") 
        return decoded
    except jwt.ExpiredSignatureError:
        logger.exception("error in verify_token")
    except jwt.InvalidTokenError:
        logger.exception("invalid token")
