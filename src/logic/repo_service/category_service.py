from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.domain.entities.base_lxml import CategoryModelWithId
from src.domain.entities.lxml_entities import CategoryEntity
from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import CategoryRepository


@dataclass(eq=False)
class CategoryService:
    repository: CategoryRepository

    async def get_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            category = await self.repository.get_category(
                entity=entity, session=session
            )
            return category
        except SQLException as e:
            raise e.message

    async def get_categories(
        self, entity: CategoryEntity, session: AsyncSession, filters: PaginationFilters
    ) -> list[CategoryModelWithId] | None:
        try:

            categories = await self.repository.get_categories(
                entity=entity, session=session, filters=filters
            )
            return categories

        except SQLException as e:
            raise e.message

    async def create_category(
        self,
        entity: CategoryEntity,
        session: AsyncSession,
    ) -> CategoryModelWithId | None:
        try:
            category = await self.repository.get_or_create(
                entity=entity, session=session
            )

            return category if category else None
        except SQLException as e:
            raise e.message

    async def update_category(
        self,
        entity: CategoryEntity,
        session: AsyncSession,
    ) -> CategoryModelWithId | None:
        try:
            category = await self.repository.update_category(
                entity=entity, session=session
            )
            return category if category else None
        except SQLException as e:
            raise e.message

    async def delete_category(
        self,
        entity: CategoryEntity,
        session: AsyncSession,
    ) -> CategoryModelWithId | None:
        try:
            category = await self.repository.delete_category(
                entity=entity, session=session
            )
            return category if category else None
        except SQLException as e:
            raise e.message
