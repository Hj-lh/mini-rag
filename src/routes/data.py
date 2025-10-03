from fastapi import APIRouter, FastAPI, UploadFile, Request
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk, Asset
from models.AssetModel import AssetModel


logger = logging.getLogger("uvicorn.error")
data_router = APIRouter(prefix="/data", tags=["Data"])

@data_router.post("/upload/{project_id}")
async def upload_file(request: Request, project_id: str, file: UploadFile):
    app_settings = get_settings()

    project_model = await ProjectModel.create_indexes(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(project_id=project_id)

    data_controller = DataController()
    is_valid, message = data_controller.validate_UploadedFile(file=file)
    if not is_valid:
        return JSONResponse(
            content = {
                "status": "error",
                "message": message,
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        original_file_name=file.filename,
        project_id=project_id,
    )
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILES_DEFAULT_CHUNK_SIZE):  # Read file in chunks
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Failed to upload file: {str(e)}"
            }
        )
    
    # store asset record in db
    asset_model = await AssetModel.create_indexes(
        db_client=request.app.db_client
    )
    asset = Asset(
        asset_project_id=project.id,
        asset_type="file",
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset)

    return JSONResponse(
        content={
            "status": "success",
            "file_id": str(asset_record.id),
            "file_id_no": file_id,
            "file_name": file.filename,
        }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):

    chunk_size = process_request.chunk_size
    overlap_size = process_request.over_lap_size
    do_reset = process_request.do_reset



    project_model = await ProjectModel.create_indexes(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )
    

    project_files_ids = []
    if process_request.file_id:
        project_files_ids = [process_request.file_id]
    else:
        asset_model = await AssetModel.create_indexes(
            db_client=request.app.db_client
        )
        project_assets = await asset_model.get_all_assets_by_project_id(
            asset_project_id=project.id,
            asset_type="file"
        )
        project_files_ids = [record["asset_name"] for record in project_assets]

    if len(project_files_ids) == 0:
        return JSONResponse(
            content={
                "status": "error",
                "message": f"No files found for project '{project_id}'. Please upload files first."
            }
        )


    process_controller = ProcessController(project_id=project_id)
    no_records = 0
    no_files = 0
    chunk_model = await ChunkModel.create_indexes(
        db_client=request.app.db_client
    )
    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    for file_id in project_files_ids:
        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Failed to load content for file '{file_id}'. Unsupported file type or file not found.")
            continue

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )

        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                content={
                    "status": "error",
                    "message": f"Failed to process file '{file_id}'. Unsupported file type or empty content."
                }
            )

        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i + 1,
                chunk_project_id=project.id
            )
            for i, chunk in enumerate(file_chunks)
        ]




        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "status": "success",
            "project_id": str(project.id),
            "no_of_files_processed": no_files,
            "no_of_chunks_created": no_records
        }
    )