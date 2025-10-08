from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnum import VectorDBEnum, DistanceMethodEnum
import logging


class QdrantDB(VectorDBInterface):

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
    def insert_one(self, collection_name: str, texts: str, vector: list, metadata: dict = None, record_ids: list = None, batch_size: int = 50) -> str:
        if not self.is_collection_exists(collection_name):
            raise ValueError(f"Collection {collection_name} does not exist.")
        return self.client.upload_records(collection_name=collection_name,
                                        records = [models.Record(
                                            vector=vector, 
                                            payload={
                                                "text": texts,
                                                "metadata": metadata
                                            },
                                        )])
    