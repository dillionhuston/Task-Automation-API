"""Database setup and engine creation."""


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL
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
