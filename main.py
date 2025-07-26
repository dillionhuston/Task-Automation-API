from fastapi import FastAPI
from app.routers import auth, user
from app.models import Base,engine


app = FastAPI()
app.include_router(auth, prefix="/auth", tags=["auth"])
app.include_router(user, prefix="/user")

Base.metadata.create_all(bind=engine)

@app.get("/health")
def get_health():
    return {"success": 200}