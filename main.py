from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.files import router as file_router
from app.routers.tasks import router as task_router
from app.models.database import Base, engine
from app.models import UserModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(file_router)
app.include_router(task_router)

@app.get("/health")
def get_health():
    return {"success": 200}
