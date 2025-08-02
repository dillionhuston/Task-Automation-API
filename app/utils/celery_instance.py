from celery import Celery

celery_app = Celery(
    'tasks',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0", # change to memory temp for testing 
    include=['app.tasks.tasks']  
)

