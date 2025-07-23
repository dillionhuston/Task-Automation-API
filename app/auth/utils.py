"""Contains user auth and jwt genrations"""


import jwt
import os 
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")


def hash_password(password: str):
    return pbkdf2_sha256.hash(password)

def verify_password(password, password_hash: str)->bool:
    return pbkdf2_sha256.verify(password, password_hash)


def jwt_generate(payload: dict):
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token: str)-> dict:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("token has experired")
    except jwt.InvalidTokenError:
        raise ValueError("invalid token")