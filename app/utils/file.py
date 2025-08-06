# This file contains the logic for file hashing, saving, and validation.

from app.utils import *  # Consider importing only what you need to keep things clear
import hashlib
import os
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from app.utils.logger import SingletonLogger

logger = SingletonLogger.get_logger()

def compute(file, algorithm: str = "sha256") -> str:
    """
    Compute the hash digest of a file using the specified algorithm.
    Args:
        file: A file-like object opened in binary mode.
        algorithm (str): Hashing algorithm to use (default is "sha256").
    Returns:
        str: The hexadecimal digest string of the file hash.
    """
    hasher = hashlib.new(algorithm)
    while chunk := file.read(8192):
        hasher.update(chunk)
    return hasher.hexdigest()


def save_file(file: UploadFile, user_id: str) -> tuple[str, str]:
    """
    Save an uploaded file to the local 'uploads' directory with a unique timestamped filename.
    Args:
        file (UploadFile): The uploaded file from FastAPI.
        user_id (str): The ID of the user uploading the file.
    Returns:
        tuple[str, str]: The filename used for saving and the full file path.
    """

    filename = f"{user_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        logger.info(f"file saved{filename}")
    return filename, file_path


def validate_file(file: UploadFile) -> None:
    """
    Validate the size of an uploaded file.
    Args:
        file (UploadFile): The uploaded file from FastAPI.
    Raises:
        HTTPException: If the file size exceeds the maximum allowed size.
    """
    max_size = 5 * 1024 * 1024  # 5 MB max file size
    if file.spool_max_size and file.spool_max_size > max_size:
        logger.critical("file too big to upload")
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too big")
