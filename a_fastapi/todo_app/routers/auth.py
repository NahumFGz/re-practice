from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/auth/")
async def get_user():
    return {"user": "authenticated"}
