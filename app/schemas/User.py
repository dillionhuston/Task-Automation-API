from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    id: str

class User(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  


