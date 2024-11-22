from abc import abstractmethod
from dataclasses import dataclass
from typing import Any


from src.common.settings.logger import get_logger
from src.infra.db.mongo.db import AsyncMongoClient

logger = get_logger(__name__)


@dataclass(eq=False)
class MongoRepository:
    client: AsyncMongoClient

    @abstractmethod
    async def add_one(self, data: dict[Any, Any]): ...
    @abstractmethod
    async def get_one(self, data: dict[Any, Any]): ...
    @abstractmethod
    async def get_many(self, data: dict[Any, Any], filters: dict[str, int]): ...
    @abstractmethod
    async def delete_one(self, data: dict[Any, Any]): ...
    @abstractmethod
    async def update_one(self, filter_data: dict[Any, Any], data: dict[Any, Any]): ...
