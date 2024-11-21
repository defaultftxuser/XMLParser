from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src.common.settings.config import ProjectSettings


@dataclass(eq=False)
class AsyncPostgresClient:
    settings: ProjectSettings

    @property
    def get_engine(self):
        return create_async_engine(
            self.settings.get_sql_db_url,
        )

    @property
    def get_async_sessionmaker(self) -> async_sessionmaker[AsyncSession | Any]:
        return async_sessionmaker(bind=self.get_engine, class_=AsyncSession)

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.get_async_sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.commit()
            await session.close()
