import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///task_automation.db")
