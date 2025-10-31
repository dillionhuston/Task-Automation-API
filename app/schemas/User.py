"""
Schemas for user-related data models.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a user."""
    username: str
    email: str
    password: str
    is_admin: bool = False


class User(BaseModel):
    """Schema for returning user data."""
    id: str
    username: str
    email: str
    is_admin: bool

    model_config = {"from_attributes": True}

__all__ = ["UserCreate", "User"]
