from dataclasses import dataclass

import motor
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.common.settings.config import ProjectSettings


@dataclass(eq=False)
class AsyncMongoClient:
    settings: ProjectSettings
    collection: str

    @property
    def get_collection(self) -> AsyncIOMotorCollection:
        return motor.motor_asyncio.AsyncIOMotorClient(self.settings.get_no_sql_db_url)[
            self.settings.mongo_database
        ][self.collection]
