from abc import ABC, abstractmethod

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self, config: dict):
        """Connect to the vector database using the provided configuration."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the vector database."""
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in the vector database."""
        pass

    @abstractmethod
    def list_all_collections(self) -> list:
        """List all collections in the vector database."""
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        """Get information about a specific collection."""
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """Delete a specific collection from the vector database."""
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        """Create a new collection in the vector database."""
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, texts: str, vectors: list, metadata: dict = None, record_ids: list = None, batch_size: int = 50) -> str:
        """Insert a single vector into the specified collection."""
        pass

    