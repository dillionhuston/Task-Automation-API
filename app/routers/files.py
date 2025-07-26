from routers import APIRouter, UploadFile, Depends, get_current_user, Session, File, User, get_db



router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User =  Depends(get_current_user),
):
    if not file:
        raise HTTPException(status_code=404, detail="file missing or error")
    

@router.get("/list")
def list_files():
    return


@router.delete("/delete{file_id}")
def delete():
    return 