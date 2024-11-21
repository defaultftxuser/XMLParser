from dataclasses import dataclass
from datetime import date

from src.infra.db.postgres.db import AsyncPostgresClient
from src.infra.repository.postgres.raw_sql import QueryRepository


@dataclass(eq=False)
class QuerySQLService:
    repository: QueryRepository
    uow: AsyncPostgresClient

    async def get_date_total_revenue(self, input_date: date):
        async with self.uow.get_async_session() as session:
            return await self.repository.get_date_total_revenue(
                session=session, input_date=input_date
            )

    async def get_date_top_three_products(self, input_date: date):
        async with self.uow.get_async_session() as session:
            return await self.repository.get_date_top_three_products(
                session=session, input_date=input_date
            )

    async def get_category_distribution_date(self, input_date: date):
        async with self.uow.get_async_session() as session:
            return await self.repository.get_category_distribution_date(
                session=session, input_date=input_date
            )
