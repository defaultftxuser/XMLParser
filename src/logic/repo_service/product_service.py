from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    ProductModelWithId,
    ProductEntityWithCategoryId,
    ProductQuery,
    ProductEntityWithoutCategoryId,
)

from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import ProductRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class ProductService:
    repository: ProductRepository
    session: "(_P: Any) -> Any"

    async def get(
        self,
        entity: ProductQuery,
        limit: int | None = 10,
        offset: int | None = 0,
    ) -> list[ProductModelWithId] | None:
        logger.debug(f"Fetching products. Entity: {entity}")
        async with self.session() as session:

            try:
                products_list = await self.repository.get(
                    entity=entity,
                    session=session,
                    offset=offset,
                    limit=limit,
                )
                logger.info(f"Successfully fetched {len(products_list)} products")
                return products_list
            except SQLException as e:
                logger.error(f"Error fetching products. Entity: {entity}, Error: {e}")
                raise e.message

    async def create_product(
        self, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        logger.debug(f"Creating product. Entity: {entity}")
        async with self.session() as session:

            try:
                product = await self.repository.create_one(
                    entity=entity, session=session
                )
                logger.info(f"Successfully created product: {product}")
                return product
            except IntegrityError as e:
                logger.error(
                    f"Integrity error while creating product. Entity: {entity}, Error: {e}"
                )
                raise IntegrityError
            except SQLException as e:
                logger.error(f"Error creating product. Entity: {entity}, Error: {e}")
                raise e.message

    async def update_product(
        self,
        entity: ProductEntityWithoutCategoryId,
        change_entity: ProductEntityWithoutCategoryId,
    ) -> ProductModelWithId | None:
        logger.debug(f"Updating product. Entity: {entity}")
        async with self.session() as session:

            try:
                product = await self.repository.update_one(
                    entity=entity, session=session, change_entity=change_entity
                )
                logger.info(f"Successfully updated product: {product}")
                return product
            except SQLException as e:
                logger.error(f"Error updating product. Entity: {entity}, Error: {e}")
                raise e.message

    async def create_or_update_product(
        self,
        entity: ProductEntityWithCategoryId,
    ) -> ProductModelWithId | None:
        logger.debug(f"Updating product. Entity: {entity}")
        async with self.session() as session:

            try:
                product = await self.repository.create_or_update(
                    entity=entity, session=session
                )
                logger.info(f"Successfully updated product: {product}")
                return product
            except SQLException as e:
                logger.error(f"Error updating product. Entity: {entity}, Error: {e}")
                raise e.message

    async def delete_product(self, entity: ProductQuery) -> ProductModelWithId | None:
        logger.debug(f"Deleting product. Entity: {entity}")
        async with self.session() as session:

            try:
                product = await self.repository.delete_one(
                    entity=entity, session=session
                )
                logger.info(f"Successfully deleted product: {product}")
                return product
            except SQLException as e:
                logger.error(f"Error deleting product. Entity: {entity}, Error: {e}")
                raise e.message
