"""
File management endpoints for Task Automation API.
Includes upload, list, and delete functionality.
"""


from io import BytesIO
from typing import List, Dict, Any

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.dependencies.auth_utils import get_current_user
from app.models.database import get_db
from app.models.user import UserModel
from app.models.file import FileModel

from app.Encryption_Services.encryptionService import EncryptionService

from app.utils.logger import SingletonLogger
from app.dependencies.constants import (
    HTTP_STATUS_BAD_REQUEST,
)

router = APIRouter(prefix="/files", tags=["Files"])
logger = SingletonLogger().get_logger()



@router.get("/list")
def list_files(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """List files uploaded by the current user."""
    try:
        files = db.query(FileModel).filter(FileModel.user_id == user.id).all()
        
        # return empty list if no files found  don't raise an exception
        if not files:
            logger.info("No files found for user %s", user.id)
            return []
        
        return [
            {
                "id": f.id,
                "filename": f.filename,
                "file_path": f.file_path,
                "file_hash": f.file_hash
            }  
            for f in files
        ]
    except Exception as exc:
        logger.error("Error querying files for user %s: %s", user.id, str(exc))
        raise HTTPException(
            status_code=HTTP_STATUS_BAD_REQUEST,
            detail="Error retrieving files"
        ) from exc


@router.get("/download/{file_id}")
async def download_file(
    file_id: str,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)):


    file = db.query(FileModel).filter(
        FileModel.id == file_id).first()

    if not file:
        raise HTTPException(404, "File not found")

    try:
        # convert stored hex nonce to bytes
        nonce_bytes = bytes.fromhex(file.nonce)

        decrypted = EncryptionService.decrypt(
            file_path=file.file_path,
            user_id=str(user.id),
            db=db,
            nonce=nonce_bytes
        )

        original_filename = file.filename or "downloaded_file"

        # guess correct MIME type
        import mimetypes
        media_type, _ = mimetypes.guess_type(original_filename)
        if media_type is None:
            media_type = "application/octet-stream"

        return StreamingResponse(
            BytesIO(decrypted),
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{original_filename}"'
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Download failed for file %s (user %s): %s", file_id, user.id, e)
        raise HTTPException(status_code=500, detail="Failed to decrypt file")
