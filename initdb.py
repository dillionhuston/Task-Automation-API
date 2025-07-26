from app.models.database import Base, engine
from app.models import user  # Import your models
from app.models import file

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
