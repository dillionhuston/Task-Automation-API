"""File upload scehema"""
from pydantic import BaseModel

class File(BaseModel):
    """Schema representing a file."""
    filename: str
