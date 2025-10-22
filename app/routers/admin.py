from fastapi import APIRouter

router = APIRouter()  

@router.get("/admin")
async def admin_endpoint():
    return {"message": "Admin panel"}
