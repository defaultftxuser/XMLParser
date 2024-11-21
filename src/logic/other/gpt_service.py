from dataclasses import dataclass
from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from src.common.settings.logger import get_logger
from src.infra.db.postgres.db import AsyncPostgresClient
from src.infra.repository.postgres.raw_sql import QueryRepository

logger = get_logger(__name__)


@dataclass(eq=False)
class QuerySQLService:
    repository: QueryRepository
    uow: AsyncPostgresClient

    async def get_date_total_revenue(self, input_date: date):
        try:
            logger.info(f"Getting total revenue for date: {input_date}")
            async with self.uow.get_async_session() as session:
                revenue = await self.repository.get_date_total_revenue(
                    session=session, input_date=input_date
                )
                logger.debug(f"Total revenue for {input_date}: {revenue}")
                return revenue
        except SQLAlchemyError as e:
            logger.error(f"Error getting total revenue for date {input_date}: {e}")
            raise
        except Exception as e:
            logger.error(f"Exception occurred : {e}")
            raise

    async def get_date_top_three_products(self, input_date: date):
        try:
            logger.info(f"Getting top 3 products for date: {input_date}")
            async with self.uow.get_async_session() as session:
                top_products = await self.repository.get_date_top_three_products(
                    session=session, input_date=input_date
                )
                logger.debug(f"Top 3 products for {input_date}: {top_products}")
                return top_products
        except SQLAlchemyError as e:
            logger.error(f"Error getting Top 3 products for date {input_date}: {e}")
            raise
        except Exception as e:
            logger.error(f"Exception occurred : {e}")
            raise

    async def get_category_distribution_date(self, input_date: date):
        try:
            logger.info(f"Getting category distribution for date: {input_date}")
            async with self.uow.get_async_session() as session:
                category_distribution = (
                    await self.repository.get_category_distribution_date(
                        session=session, input_date=input_date
                    )
                )
                logger.debug(
                    f"Category distribution for {input_date}: {category_distribution}"
                )
                return category_distribution
        except SQLAlchemyError as e:
            logger.error(f"Error category distribution for date {input_date}: {e}")
            raise
        except Exception as e:
            logger.error(f"Exception occurred : {e}")
            raise
