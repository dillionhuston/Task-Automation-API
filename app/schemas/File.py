from schemas import StringConstraints, EmailStr, BaseModel, Annotated

class File():
    owner_id: int
    filename: str
    