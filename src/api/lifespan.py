from src.infra.db.postgres.db import AsyncPostgresClient
from src.infra.db.postgres.models.base import Base
from src.logic.container import init_container


async def run_migrations():
    client: AsyncPostgresClient = init_container().resolve(AsyncPostgresClient)
    async with client.get_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
