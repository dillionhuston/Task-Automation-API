<<<<<<< Updated upstream
"""
Schemas for user creation and user data models.
"""
=======
from app.schemas import StringConstraints, EmailStr, BaseModel, Annotated
from typing import Optional
>>>>>>> Stashed changes

from typing import Annotated
from pydantic import BaseModel, EmailStr
from app.schemas import StringConstraints


# pylint: disable=too-few-public-methods
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=50)]
<<<<<<< Updated upstream
    id: str  # TODO: Change to UUID in the future
=======


    id: str  # TODO: change to UUID in the future
    is_admin: bool
>>>>>>> Stashed changes


# pylint: disable=too-few-public-methods
class User(BaseModel):
    """Schema representing a user."""
    username: str
    email: EmailStr
<<<<<<< Updated upstream
=======
    is_admin: Optional[bool] #allows to be none
>>>>>>> Stashed changes

    class Config:
        """Pydantic config to allow attribute access."""
        from_attributes = True
