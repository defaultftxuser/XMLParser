from dataclasses import dataclass


from src.common.filters.pagination import PaginationFilters
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    ProductEntityWithCategoryId,
    ProductModelWithId,
    BaseLxmlEntity,
)
from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import ProductCategoryRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class ProductCategoryService:
    repository: ProductCategoryRepository
    session: "(_P: Any) -> Any"

    async def get_products_with_category(
        self,
        filters: PaginationFilters,
        entity: ProductEntityWithCategoryId | None,
    ) -> list[ProductModelWithId] | None:
        logger.debug(
            f"Fetching products with category. Filters: {filters}, Entity: {entity}"
        )
        async with self.session() as session:
            try:
                products_list = await self.repository.get_products_with_category(
                    entity=entity.to_dict() if entity else None,
                    session=session,
                    filters=filters,
                )
                logger.info(
                    f"Successfully fetched {len(products_list)} products with categories"
                    if products_list
                    else "No products found with the specified criteria."
                )
                return products_list
            except SQLException as e:
                logger.error(
                    f"Error fetching products with category. Filters: {filters}, Entity: {entity}, Error: {e}"
                )
                raise e.message

    async def create_category_product(self, entity: BaseLxmlEntity):
        logger.debug(f"Creating category. Entity: {entity}")
        async with self.session() as session:

            try:
                category = await self.repository.create_category_and_product(
                    entity=entity, session=session
                )
                if not category:
                    logger.warning(f"Category creation returned None. Entity: {entity}")
                return category
            except SQLException as e:
                logger.error(f"Error creating categorise {e.message}")
                raise
            except Exception as e:
                logger.error(f"Exception occurred : {e}")
                raise
