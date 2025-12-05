from app.models.database import Base, engine
from app.models import user  # Import your models
from app.models import file
from app.models import tasks

Base.metadata.create_all(bind=engine)

