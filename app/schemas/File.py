"""
Schemas for file-related data models.
"""

from pydantic import BaseModel


class FileResponse(BaseModel):
    """Schema for returning file data."""
    id: str
    filename: str
    file_path: str
    file_hash: str

__all__ = ["FileResponse"]
