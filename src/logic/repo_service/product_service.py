from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.domain.entities.base_lxml import (
    ProductModelWithId,
    ProductEntityWithCategoryId,
)

from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import ProductRepository


@dataclass(eq=False)
class ProductService:
    repository: ProductRepository

    async def get_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        try:
            product = await self.repository.get_product(entity=entity, session=session)
            return product
        except SQLException as e:
            raise e.message

    async def get_products(
        self,
        entity: ProductEntityWithCategoryId,
        session: AsyncSession,
        filters: PaginationFilters,
    ) -> list[ProductModelWithId] | None:
        try:
            products_list = await self.repository.get_products(
                entity=entity, session=session, filters=filters
            )
            return products_list
        except SQLException as e:
            raise e.message

    async def create_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        try:
            product = await self.repository.create_product(
                entity=entity, session=session
            )
            return product
        except IntegrityError as e:
            raise e("Product and category must be unique")
        except SQLException as e:
            raise e.message

    async def update_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        try:
            product = await self.repository.update_product(
                entity=entity, session=session
            )
            return product
        except SQLException as e:
            raise e.message

    async def delete_product(
        self, entity: ProductEntityWithCategoryId, session: AsyncSession
    ) -> ProductModelWithId | None:
        try:
            product = await self.repository.delete_product(
                entity=entity, session=session
            )
            return product
        except SQLException as e:
            raise e.message
