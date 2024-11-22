from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.settings.logger import get_logger

logger = get_logger(__name__)


@dataclass(eq=False)
class PostgresRepo:
    model: Any

    @abstractmethod
    async def get(
        self,
        session: AsyncSession,
        entity: dict[Any, Any],
        limit: int,
        offset: int,
    ) -> Sequence[RowMapping]: ...

    @abstractmethod
    async def create_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None: ...

    @abstractmethod
    async def update_one(
        self,
        session: AsyncSession,
        entity: dict[Any, Any],
        change_entity: dict[Any, Any],
    ) -> dict[Any, Any] | None: ...

    @abstractmethod
    async def delete_one(
        self, session: AsyncSession, entity: dict[Any, Any]
    ) -> dict[Any, Any] | None: ...
