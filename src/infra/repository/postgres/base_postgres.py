from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import select, delete, update, RowMapping
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.pagination import PaginationFilters
from src.common.settings.logger import get_logger

logger = get_logger(__name__)


@dataclass(eq=False)
class PostgresRepo:
    model: Any

    async def get_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        try:
            result = await session.execute(
                select(self.model.__table__.columns).filter_by(**entity)
            )
            return result.mappings().fetchone()
        except SQLAlchemyError as e:
            logger.debug(
                f"Error fetching one from {self.model.__name__} with {entity}: {e}"
            )
            raise

    async def get_many(
        self, session: AsyncSession, entity: dict[Any, Any], filters: PaginationFilters
    ) -> Sequence[RowMapping]:
        try:
            result = await session.execute(
                select(self.model.__table__.columns)
                .filter_by(**entity)
                .offset(filters.offset)
                .limit(filters.limit)
            )
            return result.mappings().all()
        except SQLAlchemyError as e:
            logger.debug(
                f"Error fetching many from {self.model.__name__} with {entity}: {e}"
            )
            raise

    async def create_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        try:
            result = await session.execute(
                insert(self.model)
                .values(**entity)
                .returning(self.model.__table__.columns)
            )
            return result.mappings().fetchone()
        except SQLAlchemyError as e:
            logger.debug(
                f"Error creating one in {self.model.__name__} with {entity}: {e}"
            )
            raise

    async def update_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        try:
            result = await session.execute(
                update(self.model)
                .values(**entity)
                .returning(self.model.__table__.columns)
            )
            return result.mappings().fetchone()
        except SQLAlchemyError as e:
            logger.debug(
                f"Error updating one in {self.model.__name__} with {entity}: {e}"
            )
            raise

    async def delete_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        try:
            result = await session.execute(
                delete(self.model)
                .filter_by(**entity)
                .returning(self.model.__table__.columns)
            )
            return result.mappings().fetchone()
        except SQLAlchemyError as e:
            logger.debug(
                f"Error deleting one from {self.model.__name__} with {entity}: {e}"
            )
            raise
