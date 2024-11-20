from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient

from src.common.settings.config import ProjectSettings


@dataclass(eq=False)
class AsyncMongoClient:
    settings: ProjectSettings
    client: AsyncIOMotorClient

    @property
    async def get_collection(self):
        collection = self.settings.mongo_collection
        return self.client[collection]

