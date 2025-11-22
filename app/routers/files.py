"""
File management endpoints for Task Automation API.
Includes upload, list, and delete functionality.
"""

import os
from uuid import uuid4
from typing import List, Dict, Any

from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, status
from sqlalchemy.orm import Session

from dependencies.auth_utils import get_current_user
from models.database import get_db
from models.file import FileModel
from utils.file import validate_file, save_file, compute
from utils.logger import SingletonLogger
from dependencies.constants import (
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_NOT_FOUND,
)

router = APIRouter()
logger = SingletonLogger().get_logger()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
) -> Dict[str, Any]:
    """Upload a file: validate, hash, save to disk, and store metadata."""
    if not file:
        logger.exception("Tried to upload file, but nothing provided")
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="No file uploaded, or invalid file"
        )

    validate_file(file)
    file_hash = compute(file.file)
    file.file.seek(0)
    filename, file_path = save_file(file, user.id)

    new_file = FileModel(
        id=str(uuid4()),
        user_id=user.id,
        filename=filename,
        file_path=file_path,
        file_hash=file_hash,
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    logger.info(
        "New file upload | user: %s | FILE_ID: %s | path: %s",
        new_file.user_id, new_file.id, new_file.file_path
    )
    return {"message": "File uploaded successfully", "file_id": new_file.id}


@router.get("/list")
def list_files(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """List files uploaded by the current user."""
    try:
        files = db.query(FileModel).filter(FileModel.user_id == user.id).all()
        return [
            {
                "id": f.id,
                "filename": f.filename,
                "file_path": f.file_path,
                "file_hash": f.file_hash,
            }
            for f in files
        ]
    except Exception as exc:
        logger.error("No files found for user %s", user.id)
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="No files found"
        ) from exc


@router.delete("/delete/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
) -> None:
    """Delete a file by ID if it belongs to the user."""
    file = db.query(FileModel).filter(
        FileModel.id == file_id, FileModel.user_id == user.id
    ).first()

    if not file:
        logger.exception("Could not find File_ID: %s", file_id)
        raise HTTPException(
            status_code=HTTP_STATUS_NOT_FOUND,
            detail=f"File not found with ID: {file_id}"
        )

    try:
        os.remove(file.file_path)
        logger.info("Deleted file from disk | ID: %s | user: %s", file.id, file.user_id)
    except FileNotFoundError:
        logger.warning("File not found on disk (already deleted?): %s", file.file_path)
    except Exception as exc:
        logger.exception("Unexpected error deleting file: %s", file.file_path)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Could not delete file from disk"
        ) from exc

    db.delete(file)
    db.commit()
    logger.info("Deleted file record from DB | ID: %s", file_id)
