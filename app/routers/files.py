from app.routers import APIRouter, UploadFile, Depends, get_current_user, Session, File, User, get_db
from app.routers import compute, validate_file, save_file,FileModel, uuid, os, HTTPException, status


router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not file:
        raise HTTPException(status_code=400, detail="File missing or invalid.")
    validate_file(file)
    hash = compute(file.file)
    file.file.seek(0)

    filename, file_path = save_file(file, user.id)

    new_file = FileModel(
        id=str(uuid.uuid4()),
        user_id=user.id,
        filename=filename,
        file_path=file_path,
        file_hash=hash
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return {"message": "File uploaded successfully", "file_id": new_file.id}

@router.get("/list")
def list_files(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    file = db.query(FileModel).filter(FileModel.id == file_id, FileModel.user_id == user.id).first()
    if not file:
        raise HTTPException(status_code=404, detail="file not found or unauthorized")
    try:
        os.remove(file.file_path)
    except FileNotFoundError:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")
    db.delete(file)
    db.commit()