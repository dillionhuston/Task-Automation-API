import threading
import requests
import time

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.auth import router as auth_router
from app.routers.files import router as file_router
from app.routers.tasks import router as task_router
from app.routers.admin import router as admin_router

from app.models.database import Base, engine

from CLIENT.client_poll_server import poll_server

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=poll_server, daemon=True)
    thread.start()
    print("Polling thread started in background.")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(file_router)
app.include_router(task_router)
app.include_router(admin_router)


@app.get("/health")
def get_health():
    return {"success": 200}
