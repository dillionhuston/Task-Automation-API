from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.logger import SingletonLogger

router = APIRouter()
logger = SingletonLogger().get_logger()