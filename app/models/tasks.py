from app.models import Base, engine, sessionmaker, relationship, Column, String, ForeignKey


class TaskModel(Base):
    __tablename__ = "Tasks"

    id = Column(String, primary_key=True, index=True )
    user_id = Column(String, ForeignKey("users.id"))
    task_type = Column(String)
    schedule_time = Column(String)
    status = Column(String)
