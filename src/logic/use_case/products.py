from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.common.settings.logger import get_logger
from src.domain.schemas.xml_schemas import ProductSchema
from src.infra.repository.postgres.lxml_repos import ProductCategoryRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class ProductUseCase:
    service: ProductCategoryRepository

    async def get_product_with_category(
        self, entity: ProductSchema, session: AsyncSession, filters: PaginationFilters
    ):
        logger.debug(
            f"Fetching products with categories. Filters: {filters}, Entity: {entity}"
        )
        try:
            products = await self.service.get_products_with_category(
                entity=entity.dict(), session=session, filters=filters
            )
            logger.info(f"Successfully fetched products with categories: {products}")
            return products
        except SQLAlchemyError as e:
            logger.exception(
                f"Error fetching products with categories. Entity: {entity}, Filters: {filters}, Error: {e}"
            )
            raise e
        except Exception as e:
            logger.error(
                f"Error occurred with data Entity: {entity}, Filters: {filters}, Error: {e}"
            )
            raise
