from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///task_automation.db"  # Adjust for your DB

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

# Define your models (e.g., UserModel, FileModel) here or import them

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)