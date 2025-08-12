from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.files import router as file_router
from app.routers.tasks import router as task_router
<<<<<<< Updated upstream
=======
from app.routers.admin import router as admin_router
>>>>>>> Stashed changes
from app.models.database import Base, engine
from app.models.user import UserModel
from app.models.tasks import Task
from app.models.file import FileModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(file_router)
app.include_router(task_router)
<<<<<<< Updated upstream
=======
app.include_router(admin_router)
>>>>>>> Stashed changes

@app.get("/health")
def get_health():
    return {"success": 200}


