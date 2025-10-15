from app.schemas import StringConstraints, EmailStr, BaseModel, Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    id: str
    id: str  # TODO: Change to UUID in the future
    is_admin: bool

class User(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True  


