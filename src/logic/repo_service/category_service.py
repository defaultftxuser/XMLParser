from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import CategoryModelWithId
from src.domain.entities.lxml_entities import CategoryEntity
from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import CategoryRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class CategoryService:
    repository: CategoryRepository

    async def get_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        logger.debug(f"Fetching category. Entity: {entity}")
        try:
            category = await self.repository.get_category(
                entity=entity, session=session
            )
            logger.info(f"Successfully fetched category: {category}")
            return category
        except SQLException as e:
            logger.error(f"Error fetching category. Entity: {entity}, Error: {e}")
            raise e.message

    async def get_categories(
        self, entity: CategoryEntity, session: AsyncSession, filters: PaginationFilters
    ) -> list[CategoryModelWithId] | None:
        logger.debug(f"Fetching categories. Entity: {entity}, Filters: {filters}")
        try:
            categories = await self.repository.get_categories(
                entity=entity, session=session, filters=filters
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
        session: AsyncSession,
    ) -> CategoryModelWithId | None:
        logger.debug(f"Creating category. Entity: {entity}")
        try:
            category = await self.repository.get_or_create(
                entity=entity, session=session
            )
            if category:
                logger.info(f"Successfully created or fetched category: {category}")
            else:
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
        session: AsyncSession,
    ) -> CategoryModelWithId | None:
        logger.debug(f"Updating category. Entity: {entity}")
        try:
            category = await self.repository.update_category(
                entity=entity, session=session
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
        session: AsyncSession,
    ) -> CategoryModelWithId | None:
        logger.debug(f"Deleting category. Entity: {entity}")
        try:
            category = await self.repository.delete_category(
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
