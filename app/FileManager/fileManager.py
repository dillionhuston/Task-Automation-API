from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.FileManager.fileOperations import fileOperations
from app.Encryption_Services.encryptionService import EncryptionService
from app.FileManager.databaseManager import saveToDatabase
from app.FileHasher.API.HashFile import HashHandler
from app.utils.logger import SingletonLogger
import os


"""gotta make this a celery process or seperate thread"""
class fileManager:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.encryption = EncryptionService()

    async def uploadFile(self, user_id: str, file: UploadFile):  
        logger = SingletonLogger().get_logger()
        try:
            fileOperations.validate_file(file)

            filename, file_path = fileOperations.save_file(file, user_id)
            logger.info("File successfully saved to disk: %s", file_path)

            if not os.path.exists(file_path):
                raise HTTPException(status_code=500, detail="Saved file not found on disk")

            file_hash = HashHandler(file_path).hash_file()
            logger.info("File hash computed: %s", file_hash)

            nonce = self.encryption.encrypt(
                file_path=file_path,
                user_id=user_id,
                db=self.db
            )

            if nonce is None:
                logger.error("Encryption failed: nonce is None")
                raise HTTPException(status_code=500, detail="Encryption failed")

            logger.info("Encryption successful, nonce length: %d bytes", len(nonce))

            new_file = saveToDatabase(
                original_filename=file.filename or "unnamed_file",
                user_id=user_id,
                file_path=file_path,
                file_hash=file_hash,
                db=self.db,
                nonce=nonce
            )

            logger.info("File metadata saved to DB - ID: %s", new_file.id)

            return {
                "id": new_file.id,
                "filename": filename,
                "file_path": file_path,
                "file_hash": file_hash if isinstance(file_hash, str) else file_hash.hex(),
                "nonce": nonce.hex()
            }

        except Exception as e:
            logger.exception("Upload failed with unexpected exception: %s", e)
            raise HTTPException(status_code=500, detail="Upload processing failed") from e
