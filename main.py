from models.database import SessionLocal, engine, Base
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()
Base.metadata.create_all(bind=engine)

def Get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/health")
def get_health():
    return {"sucess": 200}