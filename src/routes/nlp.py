from fastapi import FastAPI, APIRouter, status, Request
from fastapi.responses import JSONResponse
from .schemes.nlp import PushRequest, SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from controllers.NLPController import NLPController
import logging

logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(
    prefix="/nlp",
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(project_id: str, request: Request, push_request: PushRequest):

    project_model = await ProjectModel.create_indexes(db_client=request.app.db_client)

    chunk_model = await ChunkModel.create_indexes(db_client=request.app.db_client)


    project = await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Project with id {project_id} not found."}
        )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )

    
    # chunks = chunk_model.get_project_chunks(project_id=project.project_object_id)

    has_record = True
    page_no = 1
    inserted_items_count = 0
    idx = 0
    while has_record:
        chunks = await chunk_model.get_project_chunks(project_id=project.id, page_no=page_no)
        if len(chunks):
            page_no += 1

        if not chunks or len(chunks) == 0:
            has_record = False
            break

        chunk_ids = list(range(idx, idx + len(chunks)))
        idx += len(chunks)

        is_inserted = nlp_controller.index_info_vector_db(
            project=project,
            chunks=chunks,
            do_reset=push_request.do_reset,
            chunks_ids=chunk_ids
        )

        if not is_inserted:
            logger.error(f"Failed to index chunks for project {project_id} at page {page_no}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Failed to index chunks for project {project_id}."}
            )
        inserted_items_count += len(chunks)
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Successfully indexed chunks for project {project_id}.", "inserted_items_count": inserted_items_count}
    )


@nlp_router.get("/index/info/{project_id}")
async def get_index_info(project_id: str, request: Request):

    project_model = await ProjectModel.create_indexes(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )
    collection_info = nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Successfully retrieved index info for project {project_id}.", "collection_info": collection_info}
    )

@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchRequest):
    project_model = await ProjectModel.create_indexes(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )

    search_results = nlp_controller.search_vector_db_collection(
        project=project,
        text=search_request.text,
        limit=search_request.limit
    )

    if not search_results:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"Failed to retrieve search results for project {project_id}."}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Successfully retrieved search results for project {project_id}.", "search_results": search_results}
    )
