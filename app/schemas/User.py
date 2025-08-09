"""
Schemas for user creation and user data models.
"""

from typing import Annotated
from pydantic import BaseModel, EmailStr
from app.schemas import StringConstraints


# pylint: disable=too-few-public-methods
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
    id: str  # TODO: Change to UUID in the future


# pylint: disable=too-few-public-methods
class User(BaseModel):
    """Schema representing a user."""
    username: str
    email: EmailStr

    class Config:
        """Pydantic config to allow attribute access."""
        from_attributes = True
