from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def root():
    return {"message": "web dashboard"}