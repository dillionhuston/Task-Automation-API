from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.file import FileModel
from app.utils.logger import SingletonLogger

logger = SingletonLogger().get_logger()

def saveToDatabase(
        original_filename: str,   
        db: Session,
        user_id: str,
        file_path: str,
        file_hash: str,
        nonce: bytes
    ):
    
    new_file = FileModel(
        id=str(uuid4()),
        filename=original_filename,  
        user_id=user_id,
        file_path=file_path,
        file_hash=file_hash,
        nonce=nonce.hex()
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    
    logger.info(f"New File added to database: {new_file.id}")
    
    return new_file
def getFileById(file_id: str, db: Session):
    file =  db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        return None
    return file