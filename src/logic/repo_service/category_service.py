from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError

from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import CategoryModelWithId
from src.domain.entities.lxml_entities import CategoryEntity, CategoryQuery
from src.infra.repository.postgres.lxml_repos import CategoryRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class CategoryService:
    repository: CategoryRepository
    session: "(_P: Any) -> Any"

    async def get(
        self,
        entity: CategoryQuery,
        limit: int | None = 10,
        offset: int | None = 0,
    ) -> list[CategoryModelWithId] | None:
        logger.debug(f"Fetching categories. Entity: {entity}")
        async with self.session() as session:

            try:
                categories = await self.repository.get(
                    entity=entity,
                    session=session,
                    offset=offset,
                    limit=limit,
                )
                logger.info(f"Successfully fetched categories: {categories}")
                return categories
            except SQLAlchemyError as e:
                logger.error(f"Error getting categorise {e}")
                raise
            except Exception as e:
                logger.error(f"Exception occurred : {e}")
                raise

    async def create_category(
        self,
        entity: CategoryEntity,
    ) -> CategoryModelWithId | None:
        async with self.session() as session:

            logger.debug(f"Creating category. Entity: {entity}")
            try:
                category = await self.repository.create_one(
                    entity=entity, session=session
                )
                if not category:
                    logger.warning(f"Category creation returned None. Entity: {entity}")
                return category
            except SQLAlchemyError as e:
                logger.error(f"Error creating categorise {e}")
                raise
            except Exception as e:
                logger.error(f"Exception occurred : {e}")
                raise

    async def update_category(
        self,
        entity: CategoryEntity,
        changed_entity: CategoryEntity,
    ) -> CategoryModelWithId | None:
        logger.debug(f"Updating category. Entity: {entity}")
        async with self.session() as session:

            try:
                category = await self.repository.update_one(
                    entity=entity, session=session, change_entity=changed_entity
                )
                if category:
                    logger.info(f"Successfully updated category: {category}")
                else:
                    logger.warning(f"Category update returned None. Entity: {entity}")
                return category
            except SQLAlchemyError as e:
                logger.error(f"Error updating category {e}")
                raise
            except Exception as e:
                logger.error(f"Exception occurred : {e}")
                raise

    async def delete_category(
        self,
        entity: CategoryEntity,
    ) -> CategoryModelWithId | None:
        async with self.session() as session:

            logger.debug(f"Deleting category. Entity: {entity}")
            try:
                category = await self.repository.delete_one(
                    entity=entity, session=session
                )
                if category:
                    logger.info(f"Successfully deleted category: {category}")
                else:
                    logger.warning(f"Category deletion returned None. Entity: {entity}")
                return category
            except SQLAlchemyError as e:
                logger.error(f"Error deleting category {e}")
                raise
            except Exception as e:
                logger.error(f"Exception occurred : {e}")
                raise
