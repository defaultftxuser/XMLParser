from dataclasses import dataclass
from typing import Any


from src.common.settings.logger import get_logger
from src.infra.repository.mongo.base_mongo import MongoRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class GPTAnswersRepo(MongoRepository):

    async def add_one(self, entity: dict[Any, Any]):
        result = await self.client.get_collection.insert_one(entity)
        return str(result.inserted_id)

    async def get_one(self, entity: dict[Any, Any]):
        document = await self.client.get_collection.find_one(entity)
        return document

    async def get_many(self, entity: dict[Any, Any], filters: dict[str, int]):
        documents = await self.client.get_collection.find(
            entity, limit=filters["limit"], skip=filters["offset"]
        ).to_list(length=None)
        return documents

    async def delete_one(self, entity: dict[Any, Any]):
        result = await self.client.get_collection.delete_one(entity)
        return result.deleted_count > 0

    async def update_one(
        self, filter_entity: dict[Any, Any], entity: dict[Any, Any]
    ): ...
