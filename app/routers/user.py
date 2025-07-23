from fastapi import APIRouter, Depends
from schemas import User
from sqlalchemy.orm import Session
from models.database import Get_db


router = APIRouter()


