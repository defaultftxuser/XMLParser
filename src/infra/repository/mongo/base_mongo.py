from dataclasses import dataclass
from typing import Any

from src.infra.db.mongo.db import AsyncMongoClient


@dataclass(eq=False)
class MongoRepository:
    client: AsyncMongoClient

    async def add_one(self, data: dict[Any, Any]):
        result = await self.client.get_collection.insert_one(data)
        return str(result.inserted_id)

    async def get_one(self, data: dict[Any, Any]):
        document = await self.client.get_collection.find_one(data)
        return document

    async def get_many(self, data: dict[Any, Any]):
        documents = await self.client.get_collection.find(data).to_list(length=None)
        return documents

    async def delete_one(self, data: dict[Any, Any]):
        result = await self.client.get_collection.delete_one(data)
        return result.deleted_count > 0

    async def update_one(self, filter_data: dict[Any, Any], data: dict[Any, Any]):
        result = await self.client.get_collection.update_one(
            filter_data, {"$set": data}
        )
        return result.modified_count > 0
