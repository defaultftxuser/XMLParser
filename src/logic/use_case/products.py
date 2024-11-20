from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.domain.schemas.xml_schemas import ProductSchema
from src.infra.repository.postgres.lxml_repos import ProductCategoryRepository


@dataclass(eq=False)
class ProductUseCase:
    service: ProductCategoryRepository

    async def get_product_with_category(
        self, entity: ProductSchema, session: AsyncSession, filters: PaginationFilters
    ):
        return await self.service.get_products_with_category(
            entity=entity.dict(), session=session, filters=filters
        )
