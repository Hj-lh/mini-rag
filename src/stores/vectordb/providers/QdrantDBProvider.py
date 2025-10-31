from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnum import VectorDBEnum, DistanceMethodEnum
import logging


class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str , distance_method: str):
        self.client = None
        self.db_path = db_path
        self.distance_method = distance_method

        if distance_method == DistanceMethodEnum.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnum.EUCLIDEAN.value:
            self.distance_method = models.Distance.EUCLIDEAN
        elif distance_method == DistanceMethodEnum.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        raise NotImplementedError("Disconnect method is not implemented for QdrantDB.")
    
    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> list:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name):
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        if self.is_collection_exists(collection_name):
            self.client.delete_collection(collection_name=collection_name)
    
    def create_collection(self, collection_name, embedding_size, do_reset = False):
        if do_reset:
            self.delete_collection(collection_name)
        if not self.is_collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_method)
            )
            return True
        return False
    def insert_one(self, collection_name: str, texts: str, vector: list, metadata: dict = None, record_ids: list = None) -> str:
        if not self.is_collection_exists(collection_name):
            raise ValueError(f"Collection {collection_name} does not exist.")
        return self.client.upload_records(collection_name=collection_name,
                                        records = [models.Record(
                                            id=[record_ids],
                                            vector=vector, 
                                            payload={
                                                "text": texts,
                                                "metadata": metadata
                                            },
                                        )])
        return True
    
    def insert_many(self, collection_name: str, texts: list, vectors: list, metadatas: list = None, record_ids: list = None, batch_size: int = 50):
        if metadatas is None:
            metadatas = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0,len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadatas = metadatas[i:batch_end]
            batch_records_ids = record_ids[i:batch_end]

            batch_records = [
                models.Record(
                    id=batch_records_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": batch_metadatas[x]
                    }
                )
                for x in range(len(batch_texts))
            ]
            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )
            except Exception as e:
                self.logger.error(f"Error inserting batch starting at index {i}: {e}")
                return False
        return True

    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5) -> list:
        
        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
        )