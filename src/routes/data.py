from fastapi import APIRouter, FastAPI, UploadFile
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings
from controllers import DataController, ProjectController
import aiofiles
import logging

logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(prefix="/data", tags=["Data"])

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile):
    app_settings = get_settings()

    data_controller = DataController()
    is_valid, message = data_controller.validate_UploadedFile(file=file)
    if not is_valid:
        return JSONResponse(
            content = {
                "status": "error",
                "message": message
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(
        original_file_name=file.filename,
        project_id=project_id,
    )
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILES_DEFULT_CHUNK_SIZE):  # Read file in chunks
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Failed to upload file: {str(e)}"
            }
        )
    


    return JSONResponse(
        content={
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully to project '{project_id}'."
        }
    )