from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List



class NLPController(BaseController):

    def __init__(self, vectordb_client, embedding_client, generation_client):
        super().__init__()
        self.vectordb_client = vectordb_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        

    def create_collection_name(self, project_id: str) -> str:
        return f"project_{project_id}_collection".strip()
    
    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name, collection_name)

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.get_collection_info(collection_name)

    def index_info_vector_db(self, project: Project, chunks: List[DataChunk], chunks_ids: List[int], do_reset: bool = False) -> bool:
        
        # step 1: create collection if not exists
        collection_name = self.create_collection_name(project_id=project.project_id)
        # step 2: manage items
        texts = [chunk.text for chunk in chunks]
        metadata = [chunk.metadata for chunk in chunks]
        vectors = [
            self.embedding_client.embed_text(text = text, document_type = DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]
        # step 3: create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset
        )

        # step 4: insert into vector db
        _ = self.vectordb_client.insert_many(
            collection_name = collection_name,
            vectors = vectors,
            metadatas = metadata,
            documents = texts,
            record_ids = chunks_ids,
        )


        