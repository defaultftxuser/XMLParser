import pytest
from faker import Faker
from punq import Container
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.orm import sessionmaker

from src.common.settings.config_dev import DevProjectSettings

from src.infra.db.postgres.models.base import Base
from src.logic.container import init_container


@pytest.fixture()
def get_faker():
    return Faker()


@pytest.fixture(scope="session")
def get_container() -> Container:
    return init_container()


@pytest.fixture(scope="session")
async def db_engine(get_container) -> AsyncEngine:
    engine = create_async_engine(
        get_container.resolve(DevProjectSettings).get_sql_db_url, echo=True
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def db_session(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncSession:
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
