import datetime
from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import select, delete, update, RowMapping
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters


@dataclass(eq=False)
class PostgresRepo:
    model: Any

    async def get_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:

        result = await session.execute(
            select(self.model.__table__.columns).filter_by(**entity)
        )
        return result.mappings().fetchone()

    async def get_many(
        self, session: AsyncSession, entity: dict[Any, Any], filters: PaginationFilters
    ) -> Sequence[RowMapping]:

        result = await session.execute(
            select(self.model.__table__.columns)
            .filter_by(**entity)
            .offset(filters.offset)
            .limit(filters.limit)
        )
        return result.mappings().all()

    async def create_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:

        result = await session.execute(
            insert(self.model).values(**entity).returning(self.model.__table__.columns)
        )
        return result.mappings().fetchone()

    async def get_or_create(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:

        query = (
            (insert(self.model).values(**entity)).on_conflict_do_update(
                index_elements=["name"], set_={"updated_at": datetime.datetime.now()}
            )
        ).returning(self.model.__table__.c)
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def update_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:

        result = await session.execute(
            update(self.model.__table__.columns)
            .values(**entity)
            .returning(self.model.__table__.columns)
        )
        return result.mappings().fetchone()

    async def delete_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:

        result = await session.execute(
            delete(self.model.__table__.columns)
            .filter_by(**entity)
            .returning(self.model.__table__.columns)
        )
        return result.mappings().fetchone()
