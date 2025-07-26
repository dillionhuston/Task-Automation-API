"""Contains user auth and jwt generation"""
from .auth import verify_password, verify_token, jwt_generate, jwt, os, pbkdf2_sha256, load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")

def hash_password(password: str):
    return pbkdf2_sha256.hash(password)

def verify_password(password, password_hash: str) -> bool:
    return pbkdf2_sha256.verify(password, password_hash)

def jwt_generate(payload: dict):
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("invalid token")