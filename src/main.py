from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DB_NAME]

    llm_factory = LLMProviderFactory(settings)

    vector_db_provider_factory = VectorDBProviderFactory(settings)

    app.generation_client = llm_factory.create(provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)

    app.embedding_client = llm_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID, embedding_size = settings.EMBEDDING_SIZE)

    app.vectordb_client = vector_db_provider_factory.create(provider=settings.VECTOR_DB_PROVIDER)
    app.vectordb_client.connect()
    yield

    app.mongo_conn.close()
    app.vectordb_client.disconnect()
# async def shutdown_db_client():
#     app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)
# app.router.lifespan.on_startup.append(startup_db_client)
# app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)

