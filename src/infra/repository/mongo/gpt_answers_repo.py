from dataclasses import dataclass

from src.domain.entities.base_lxml import GPTAnswerEntity
from src.infra.repository.mongo.base_mongo import MongoRepository


@dataclass(eq=False)
class GPTAnswersRepo(MongoRepository):

    async def add_one(self, entity: GPTAnswerEntity):
        result = await self.client.get_collection.insert_one(entity.to_dict())
        return str(result.inserted_id)

    async def get_one(self, entity: GPTAnswerEntity):
        document = await self.client.get_collection.find_one(entity.to_dict())
        return document

    async def get_many(self, entity: GPTAnswerEntity):
        documents = await self.client.get_collection.find(entity.to_dict()).to_list(
            length=None
        )
        return documents

    async def delete_one(self, entity: GPTAnswerEntity):
        result = await self.client.get_collection.delete_one(entity.to_dict())
        return result.deleted_count > 0

    async def update_one(self, filter_entity: GPTAnswerEntity, entity: GPTAnswerEntity):
        result = await self.client.get_collection.update_one(
            filter_entity.to_dict(), {"$set": entity.to_dict()}
        )
        return result.modified_count > 0
