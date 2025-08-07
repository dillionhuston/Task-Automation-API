import hashlib
import os
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
from app.utils.logger import SingletonLogger
from app.dependencies.constants import MAX_UPLOAD_SIZE_MB, FILE_STORAGE_DIR

logger = SingletonLogger().get_logger()

def compute(file, algorithm: str = "sha256") -> str:
    """
    Compute the hash of a file using the specified algorithm.

    Args:
        file: A binary file-like object.
        algorithm (str): Hashing algorithm (default: 'sha256').

    Returns:
        str: Hexadecimal hash digest.
    """
    try:
        hasher = hashlib.new(algorithm)
        while chunk := file.read(8192):
            hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logger.exception(f"Error computing file hash: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compute file hash."
        )

def save_file(file: UploadFile, user_id: str) -> tuple[str, str]:
    """
    Save uploaded file to disk with a unique name.

    Args:
        file (UploadFile): Uploaded file.
        user_id (str): User's ID.

    Returns:
        tuple[str, str]: (Saved filename, full path)
    """
    try:
        filename = f"{user_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{file.filename}"
        os.makedirs(FILE_STORAGE_DIR, exist_ok=True)
        file_path = os.path.join(FILE_STORAGE_DIR, filename)

        with open(file_path, "wb") as f:
            contents = file.file.read()
            f.write(contents)

        logger.info(f"File saved: {filename} at {file_path}")
        return filename, file_path

    except Exception as e:
        logger.exception(f"Error saving file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file."
        )

def validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file size.

    Args:
        file (UploadFile): Uploaded file.

    Raises:
        HTTPException: If file exceeds max allowed size.
    """
    try:
        file.file.seek(0, os.SEEK_END)
        size_bytes = file.file.tell()
        file.file.seek(0)

        size_mb = size_bytes / (1024 * 1024)
        if size_mb > MAX_UPLOAD_SIZE_MB:
            logger.warning(f"Upload rejected: file too large ({size_mb:.2f} MB)")
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File exceeds max allowed size of {MAX_UPLOAD_SIZE_MB} MB"
            )
    except Exception as e:
        logger.exception(f"Error validating file size: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate file size."
        )
