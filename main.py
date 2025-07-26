from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.files import router as file_router
from app.models import Base,engine


app = FastAPI()
app.include_router(auth_router)
#app.include_router(user)
app.include_router(file_router)


@app.get("/health")
def get_health():
    return {"success": 200}