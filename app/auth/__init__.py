"""Authentication module for JWT token creation and verification."""
import os

import jwt
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
from app.config import SECRET_KEY
from app.models import UserModel
