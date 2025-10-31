"""
Celery instance module.
Provides a shared Celery app for task scheduling.
"""

from celery import Celery

celery_app = Celery(
    "task_automation",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
