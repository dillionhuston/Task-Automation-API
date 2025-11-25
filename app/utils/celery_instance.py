import os
from celery import Celery

redis_url = os.getenv("CELERY_BROKER_URL")
if not redis_url:
    # fallback for local development
    redis_url = "redis://localhost:6379/0"

celery_app = Celery(
    "task_automation",
    broker=redis_url,
    backend=redis_url
)


import app.tasks.tasks