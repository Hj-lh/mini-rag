from fastapi import APIRouter, FastAPI, UploadFile

from helpers.config import get_settings
from controllers import DataController


data_router = APIRouter(prefix="/data", tags=["Data"])

@data_router.post("/upload/{file_id}")
async def upload_file(file_id: str, file: UploadFile):
    app_settings = get_settings()

    is_valid = DataController().validate_UploadedFile(file)

    return is_valid

