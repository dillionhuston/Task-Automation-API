import threading
import requests
import time

from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.auth import router as auth_router
from routers.files import router as file_router
from routers.tasks import router as task_router
from routers.admin import router as admin_router
from models.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(auth_router)
app.include_router(file_router)
app.include_router(task_router)
app.include_router(admin_router)


@app.get("/health")
def get_health():
    return {"success": 200}