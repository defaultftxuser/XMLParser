from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    ProductModelWithId,
    ProductEntityWithCategoryId,
)

from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import ProductRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class ProductService:
    repository: ProductRepository

    async def get_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        logger.debug(f"Fetching product. Entity: {entity}")
        try:
            product = await self.repository.get_product(entity=entity, session=session)
            logger.info(f"Successfully fetched product: {product}")
            return product
        except SQLException as e:
            logger.error(f"Error fetching product. Entity: {entity}, Error: {e}")
            raise e.message

    async def get_products(
        self,
        entity: ProductEntityWithCategoryId,
        session: AsyncSession,
        filters: PaginationFilters,
    ) -> list[ProductModelWithId] | None:
        logger.debug(f"Fetching products. Entity: {entity}, Filters: {filters}")
        try:
            products_list = await self.repository.get_products(
                entity=entity, session=session, filters=filters
            )
            logger.info(f"Successfully fetched {len(products_list)} products")
            return products_list
        except SQLException as e:
            logger.error(
                f"Error fetching products. Entity: {entity}, Filters: {filters}, Error: {e}"
            )
            raise e.message

    async def create_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        logger.debug(f"Creating product. Entity: {entity}")
        try:
            product = await self.repository.create_product(
                entity=entity, session=session
            )
            logger.info(f"Successfully created product: {product}")
            return product
        except IntegrityError as e:
            logger.error(
                f"Integrity error while creating product. Entity: {entity}, Error: {e}"
            )
            raise e("Product and category must be unique")
        except SQLException as e:
            logger.error(f"Error creating product. Entity: {entity}, Error: {e}")
            raise e.message

    async def update_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        logger.debug(f"Updating product. Entity: {entity}")
        try:
            product = await self.repository.update_product(
                entity=entity, session=session
            )
            logger.info(f"Successfully updated product: {product}")
            return product
        except SQLException as e:
            logger.error(f"Error updating product. Entity: {entity}, Error: {e}")
            raise e.message

    async def delete_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        logger.debug(f"Deleting product. Entity: {entity}")
        try:
            product = await self.repository.delete_product(
                entity=entity, session=session
            )
            logger.info(f"Successfully deleted product: {product}")
            return product
        except SQLException as e:
            logger.error(f"Error deleting product. Entity: {entity}, Error: {e}")
            raise e.message
