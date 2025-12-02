"""Database setup and engine creation."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
# fix this for live backend
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL must be set — SQLite is not supported on Fly.io")

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """yield database session and make sure its closed"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
