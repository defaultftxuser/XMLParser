from dataclasses import dataclass
from typing import Any

from pymongo.errors import WriteError, OperationFailure

from src.common.settings.logger import get_logger
from src.infra.db.mongo.db import AsyncMongoClient

logger = get_logger(__name__)


@dataclass(eq=False)
class MongoRepository:
    client: AsyncMongoClient

    async def add_one(self, data: dict[Any, Any]):
        try:
            result = await self.client.get_collection.insert_one(data)
            logger.info(f"Successfully added document with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except ConnectionError as e:
            logger.debug(
                f"MongoDB connection error while adding document: {data} - {e}"
            )
            raise e
        except WriteError as e:
            logger.debug(f"MongoDB write error while adding document: {data} - {e}")
            raise e
        except OperationFailure as e:
            logger.debug(
                f"MongoDB operation failure while adding document: {data} - {e}"
            )
            raise e
        except Exception as e:
            logger.debug(f"Unexpected error while adding document: {data} - {e}")
            raise e

    async def get_one(self, data: dict[Any, Any]):
        try:
            document = await self.client.get_collection.find_one(data)
            if document:
                logger.info(f"Document found: {document}")
            else:
                logger.info(f"No document found for: {data}")
            return document
        except ConnectionError as e:
            logger.debug(
                f"MongoDB connection error while fetching document: {data} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.debug(
                f"MongoDB operation failure while fetching document: {data} - {e}"
            )
            raise e
        except Exception as e:
            logger.debug(f"Unexpected error while fetching document: {data} - {e}")
            raise e

    async def get_many(self, data: dict[Any, Any]):
        try:
            documents = await self.client.get_collection.find(data).to_list(length=None)
            logger.info(f"Fetched {len(documents)} documents")
            return documents
        except ConnectionError as e:
            logger.debug(
                f"MongoDB connection error while fetching documents: {data} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.debug(
                f"MongoDB operation failure while fetching documents: {data} - {e}"
            )
            raise e
        except Exception as e:
            logger.debug(f"Unexpected error while fetching documents: {data} - {e}")
            raise e

    async def delete_one(self, data: dict[Any, Any]):
        try:
            result = await self.client.get_collection.delete_one(data)
            if result.deleted_count > 0:
                logger.info(f"Successfully deleted document: {data}")
            else:
                logger.info(f"No document found to delete for: {data}")
            return result.deleted_count > 0
        except ConnectionError as e:
            logger.debug(
                f"MongoDB connection error while deleting document: {data} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.debug(
                f"MongoDB operation failure while deleting document: {data} - {e}"
            )
            raise e
        except Exception as e:
            logger.debug(f"Unexpected error while deleting document: {data} - {e}")
            raise e

    async def update_one(self, filter_data: dict[Any, Any], data: dict[Any, Any]):
        try:
            result = await self.client.get_collection.update_one(
                filter_data, {"$set": data}
            )
            if result.modified_count > 0:
                logger.info(f"Successfully updated document with filter {filter_data}")
            else:
                logger.info(f"No document found to update for {filter_data}")
            return result.modified_count > 0
        except ConnectionError as e:
            logger.debug(
                f"MongoDB connection error while updating document: {filter_data} - {e}"
            )
            raise e
        except WriteError as e:
            logger.debug(
                f"MongoDB write error while updating document: {filter_data} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.debug(
                f"MongoDB operation failure while updating document: {filter_data} - {e}"
            )
            raise e
        except Exception as e:
            logger.debug(
                f"Unexpected error while updating document: {filter_data} - {e}"
            )
            raise e
