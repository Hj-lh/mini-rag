from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNKS_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict())
        chunk._id = result.inserted_id
        return chunk
    
    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({
            "_id": object(chunk_id)
        })
        if result is None:
            return None
        return DataChunk(**result)
    

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            operations = [InsertOne(chunk.dict()) for chunk in batch]

            await self.collection.bulk_write(operations)

        return len(chunks)