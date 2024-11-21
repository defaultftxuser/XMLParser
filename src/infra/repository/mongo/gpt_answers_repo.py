from dataclasses import dataclass

from pymongo.errors import WriteError, OperationFailure

from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import GPTAnswerEntity
from src.infra.repository.mongo.base_mongo import MongoRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class GPTAnswersRepo(MongoRepository):

    async def add_one(self, entity: GPTAnswerEntity):
        try:
            logger.info("Attempting to add GPTAnswerEntity: %s", entity.to_dict())
            result = await self.client.get_collection.insert_one(entity.to_dict())
            logger.info(
                "Successfully added GPTAnswerEntity with ID: %s", result.inserted_id
            )
            return str(result.inserted_id)
        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while adding GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except WriteError as e:
            logger.exception(
                f"MongoDB write error while adding GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.exception(
                f"MongoDB operation failure while adding GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while adding GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e

    async def get_one(self, entity: GPTAnswerEntity):
        try:
            logger.debug(
                "Attempting to fetch one GPTAnswerEntity with filter: %s",
                entity.to_dict(),
            )
            document = await self.client.get_collection.find_one(entity.to_dict())
            if document:
                logger.info("Found GPTAnswerEntity: %s", document)
            else:
                logger.info("No GPTAnswerEntity found for filter: %s", entity.to_dict())
            return document
        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while fetching GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.exception(
                f"MongoDB operation failure while fetching GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while fetching GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e

    async def get_many(self, entity: GPTAnswerEntity):
        try:
            logger.debug(
                "Attempting to fetch many GPTAnswerEntities with filter: %s",
                entity.to_dict(),
            )
            documents = await self.client.get_collection.find(entity.to_dict()).to_list(
                length=None
            )
            logger.info("Fetched %d GPTAnswerEntities", len(documents))
            return documents
        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while fetching GPTAnswerEntities: {entity.to_dict()} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.exception(
                f"MongoDB operation failure while fetching GPTAnswerEntities: {entity.to_dict()} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while fetching GPTAnswerEntities: {entity.to_dict()} - {e}"
            )
            raise e

    async def delete_one(self, entity: GPTAnswerEntity):
        try:
            logger.debug(
                "Attempting to delete GPTAnswerEntity with filter: %s", entity.to_dict()
            )
            result = await self.client.get_collection.delete_one(entity.to_dict())
            if result.deleted_count > 0:
                logger.info("Successfully deleted GPTAnswerEntity")
            else:
                logger.info(
                    "No GPTAnswerEntity found to delete for filter: %s",
                    entity.to_dict(),
                )
            return result.deleted_count > 0
        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while deleting GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.exception(
                f"MongoDB operation failure while deleting GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while deleting GPTAnswerEntity: {entity.to_dict()} - {e}"
            )
            raise e

    async def update_one(self, filter_entity: GPTAnswerEntity, entity: GPTAnswerEntity):
        try:
            logger.debug(
                "Attempting to update GPTAnswerEntity with filter: %s, update: %s",
                filter_entity.to_dict(),
                entity.to_dict(),
            )
            result = await self.client.get_collection.update_one(
                filter_entity.to_dict(), {"$set": entity.to_dict()}
            )
            if result.modified_count > 0:
                logger.info("Successfully updated GPTAnswerEntity")
            else:
                logger.info(
                    "No GPTAnswerEntity updated for filter: %s", filter_entity.to_dict()
                )
            return result.modified_count > 0
        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while updating GPTAnswerEntity: {filter_entity.to_dict()} - {e}"
            )
            raise e
        except WriteError as e:
            logger.exception(
                f"MongoDB write error while updating GPTAnswerEntity: {filter_entity.to_dict()} - {e}"
            )
            raise e
        except OperationFailure as e:
            logger.exception(
                f"MongoDB operation failure while updating GPTAnswerEntity: {filter_entity.to_dict()} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while updating GPTAnswerEntity: {filter_entity.to_dict()} - {e}"
            )
            raise e
