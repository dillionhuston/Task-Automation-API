from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, Depends, File, HTTPException, status
from sqlalchemy.orm import Session
from app.routers import compute, validate_file, save_file, FileModel, uuid, os
from app.routers import get_current_user, get_db, User
from app.utils.logger import SingletonLogger

router = APIRouter()
logger = SingletonLogger.get_logger()


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
        raise status.HTTP_404_NOT_FOUND
    validate_file(file)
    
    file_hash = compute(file.file)
    file.file.seek(0)  # Reset file pointer after reading

    filename, file_path = save_file(file, user.id)

    new_file = FileModel(
        id=str(uuid.uuid4()),
        user_id=user.id,
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
        logger.exception(f"no file found in {user.id}")
        raise FileNotFoundError(f"no files found in {files.file_path}")


@router.delete("/delete/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:# noqa: F841
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
        logger.exception("no file found")
        raise status.HTTP_404_NOT_FOUND("file not found")
    try:
        os.remove(file.file_path)
    except FileNotFoundError:
        logger.exception("file not found, could have been deleted ")
        # File was already deleted from disk; continue
        pass
    except:
        raise status.HTTP_406_NOT_ACCEPTABLE
    db.delete(file)
    logger.info("file succesfull deleted")
    db.commit()
