from fastapi import APIRouter

from app import app

router = APIRouter()


@router.get("/")
async def root():
    return {"message": f"{app.title} {app.version}"}


@router.get("/healthcheck")
async def get_health_status():
    return {"status": "OK"}
