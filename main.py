from fastapi import FastAPI
from app.models.database import SessionLocal, engine, Base
from app.auth.routes import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
Base.metadata.create_all(bind=engine)

@app.get("/health")
def get_health():
    return {"success": 200}