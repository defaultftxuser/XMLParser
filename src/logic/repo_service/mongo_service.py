from dataclasses import dataclass

from src.common.converters.converters import convert_from_mongo_to_entity
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import GPTAnswerEntity
from src.infra.exceptions.exceptions import MongoOperationError
from src.infra.repository.mongo.gpt_answers_repo import GPTAnswersRepo

logger = get_logger(__name__)


@dataclass(eq=False)
class MongoService:
    repo: GPTAnswersRepo

    def get_query(self, sale_date: str | None, offset: int = 0, limit: int = 10):
        entity = {}
        filters = {"offset": offset, "limit": limit}
        if sale_date:
            entity["sale_date"] = sale_date
            return entity, filters
        return entity, filters

    async def get_answers(
        self, sale_date: str | None, offset: int = 0, limit: int = 10
    ) -> list[dict[str, str]]:
        entity, filters = self.get_query(sale_date, offset, limit)
        try:
            logger.debug(
                "Attempting to fetch many GPTAnswerEntities with filter: %s",
                entity,
            )
            documents = await self.repo.get_many(entity=entity, filters=filters)
            if documents:
                return [
                    convert_from_mongo_to_entity(document) for document in documents
                ]

            logger.info("Fetched %d GPTAnswerEntities", len(documents))
            return documents
        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while fetching GPTAnswerEntities: {entity} - {e}"
            )
            raise e
        except MongoOperationError as e:
            logger.exception(
                f"MongoDB operation failure while fetching GPTAnswerEntities: {entity} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while fetching GPTAnswerEntities: {entity} - {e}"
            )
            raise e

    async def add_one(self, entity: GPTAnswerEntity):
        try:
            logger.debug(
                "Attempting to add many GPTAnswerEntity: %s",
                entity,
            )
            document = await self.repo.add_one(entity=entity.to_dict())
            logger.info("Added %d GPTAnswerEntities", entity)
            return document

        except TypeError:
            raise TypeError("Wrong data type")

        except ConnectionError as e:
            logger.exception(
                f"MongoDB connection error while adding GPTAnswerEntity: {entity} - {e}"
            )
            raise e
        except MongoOperationError as e:
            logger.exception(
                f"MongoDB operation failure while adding GPTAnswerEntity: {entity} - {e}"
            )
            raise e
        except Exception as e:
            logger.exception(
                f"Unexpected error while adding GPTAnswerEntity: {entity} - {e}"
            )
            raise e
