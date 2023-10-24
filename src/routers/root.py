import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    env = os.environ["API_ENVIRONMENT"]
    return {
        "message": f"Bilinz {env} user management service",
    }
