from pydantic import BaseModel
from typing import Optional

"""Schema for returning files"""
class FileResponse(BaseModel):
    id: str
    filename: str
    file_path: str
    file_hash: str

class FileUploadRequest(BaseModel):
    filename: str
    file_hash: Optional[str] = None

__all__ = ["FileResponse", "FileUploadRequest"]
