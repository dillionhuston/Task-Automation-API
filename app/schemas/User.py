"""
Schemas for user creation and user data models.
"""
<<<<<<< HEAD
from app.schemas import StringConstraints, EmailStr, BaseModel, Annotated
from typing import Optional
=======
>>>>>>> parent of 013e964 (Add admin CLI and routes; pending admin dashboard, route restriction, and tests)

from typing import Annotated
from pydantic import BaseModel, EmailStr
from app.schemas import StringConstraints


# pylint: disable=too-few-public-methods
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
<<<<<<< HEAD
    is_admin: bool = False  # optional, defaults to False
=======
    id: str  # TODO: Change to UUID in the future

>>>>>>> parent of 013e964 (Add admin CLI and routes; pending admin dashboard, route restriction, and tests)

# pylint: disable=too-few-public-methods
class User(BaseModel):
    """Schema representing a user."""
    id: str
    username: str
    email: EmailStr
<<<<<<< HEAD
    is_admin: bool
=======
>>>>>>> parent of 013e964 (Add admin CLI and routes; pending admin dashboard, route restriction, and tests)

    class Config:
        """Pydantic config to allow attribute access."""
        from_attributes = True
        orm_mode = True
