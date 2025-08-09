"""
Celery application instance configuration.
"""

from celery import Celery

celery_app = Celery(
    'tasks',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",  # change to memory backend for testing
    include=['app.tasks.tasks']
)
