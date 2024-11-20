from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.domain.entities.base_lxml import (
    ProductEntityWithCategoryId,
    ProductModelWithId,
)
from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import ProductCategoryRepository


@dataclass(eq=False)
class ProductCategoryService:
    repository: ProductCategoryRepository

    async def get_products_with_category(
        self,
        session: AsyncSession,
        filters: PaginationFilters,
        entity: ProductEntityWithCategoryId | None,
    ) -> list[ProductModelWithId] | None:
        try:
            products_list = await self.repository.get_products_with_category(
                entity=entity.to_dict(), session=session, filters=filters
            )
            return products_list
        except SQLException as e:
            raise e.message
