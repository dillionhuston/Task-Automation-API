from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, status
from sqlalchemy.orm import Session
from app.routers import compute, validate_file, save_file, FileModel, uuid, os
from app.routers import get_current_user, get_db, User
from app.utils.logger import SingletonLogger
from app.dependencies.constants import( 
    JSON_USER_ID,
    HTTP_STATUS_BAD_REQUEST,
    FILE_STORAGE_DIR,
    HTTP_STATUS_NOT_FOUND,
    HTTP_STATUS_NOT_APPLICABLE

)

router = APIRouter()
logger = SingletonLogger().get_logger()

@router.post("/upload") 
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:# noqa: F841
    """
    Upload a file: validate, hash, save to disk, and store metadata.
    Args:
        file (UploadFile): File from client.
        db (Session): Active DB session.
        user (User): Authenticated user.
    Returns:
        dict: Success message and file ID.
    Raises:
        HTTPException: On validation failure or missing file.
      """
    if not file:
        logger.exception("treid to upload file, but nothing provided")
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="no file uploaded, or is not a file"
        )
    validate_file(file)
    
    file_hash = compute(file.file)
    file.file.seek(0)  # Reset file pointer after reading
    filename, file_path = save_file(file, user.id)

    new_file = FileModel(
        id=str(uuid.uuid4()),
        JSON_USER_ID=user.id,
        filename=filename,
        file_path=file_path,
        file_hash=file_hash,
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    logger.info(f"new file upload for user: {new_file.user_id}, FILE_ID: {new_file.id}, filepath:{new_file.file_path}")
    return {"message": "File uploaded successfully", "file_id": new_file.id}


@router.get("/list")
def list_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Dict[str, Any]]:# noqa: F841
    """
    List files uploaded by the current user.

    Args:
        user (User): Authenticated user.
        db (Session): Active DB session.

    Returns:
        List[dict]: File metadata (ID, name, path, hash).

    Raises:
        FileNotFoundError: If DB query fails.
        """
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
    except:
        logger.error(f"No files found in {FILE_STORAGE_DIR} for {user.id}")
        raise HTTPException(
            status=HTTP_STATUS_BAD_REQUEST,
            details=f"File not found in {FILE_STORAGE_DIR}"
        )
       


@router.delete("/delete/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),) -> None:# noqa: F841
    """
    Delete a file by ID if it belongs to the user.
    Args:
        file_id (str): Target file's UUID.
        db (Session): Active DB session.
        user (User): Authenticated user.
    Returns:
        None
    Raises:
        HTTPException: If file not found or delete fails.
    """

    file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == user.id).first()
    if not file:
        logger.exception(f"Could not find File_ID: {file_id}")
        raise HTTPException(
            status_code=HTTP_STATUS_NOT_FOUND,
            detail = f"File not found with {file_id} "
        )
    
    try:
        os.remove(file.file_path)
        logger.info(f"successfully deleted {file.id}, from {file.user_id} account")

    except FileNotFoundError:
        logger.exception("file not found, could have been deleted ")
        # File was already deleted from disk; continue

    except Exception as e:
        logger.exception(f"unexpected error deleting file: {file.file_path}")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Could not delete file from disk"
        )
    
    db.delete(file)
    db.commit()
    logger.info(f"Deleted file record from DB for file_id: {file_id}")

    
