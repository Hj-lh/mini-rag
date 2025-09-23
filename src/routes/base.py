from fastapi import FastAPI, APIRouter
from helpers.config import get_settings
base_router = APIRouter()

@base_router.get("/")
async def welcome():
    app_settings = get_settings()
    return {"app_name": app_settings.APP_NAME, "app_version": app_settings.APP_VERSION}
