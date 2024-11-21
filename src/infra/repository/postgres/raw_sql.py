from dataclasses import dataclass
from datetime import date
from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.settings.logger import get_logger
from src.infra.db.postgres.models.lxml_models import Product

logger = get_logger(__name__)


@dataclass(eq=False)
class QueryRepository:
    product_model: Any
    category_model: Any

    async def get_date_total_revenue(self, session: AsyncSession, input_date: date):

        try:
            logger.debug(f"Executing total revenue query for date: {input_date}")
            query = select(
                func.sum(self.product_model.price * self.product_model.quantity) / 100
            ).where(self.product_model.sale_date == input_date)
            result = await session.execute(query)
            total_revenue = result.scalar()
            logger.info(f"Total revenue for {input_date}: {total_revenue}")
            return total_revenue
        except Exception as e:
            logger.error(f"Error in get_date_total_revenue for {input_date}: {e}")
            raise

    async def get_date_top_three_products(
        self, session: AsyncSession, input_date: date
    ):

        try:
            logger.debug(f"Executing top three products query for date: {input_date}")
            query = (
                select(
                    self.product_model.product,
                    func.sum(self.product_model.quantity / 100).label("total_sales"),
                )
                .where(self.product_model.sale_date == input_date)
                .group_by(self.product_model.product)
                .order_by(func.sum(self.product_model.quantity).desc())
                .limit(3)
            )
            result = await session.execute(query)
            top_products = result.scalars().fetchall()
            logger.info(f"Top three products for {input_date}: {top_products}")
            return top_products
        except Exception as e:
            logger.error(f"Error in get_date_top_three_products for {input_date}: {e}")
            raise

    async def get_category_distribution_date(
        self, session: AsyncSession, input_date: date
    ):
        try:
            logger.debug(
                f"Executing category distribution query for date: {input_date}"
            )
            query = await session.execute(
                select(
                    self.category_model.name,
                    func.sum(
                        self.product_model.price * self.product_model.quantity / 100
                    ).label("category_revenue"),
                )
                .join(
                    self.product_model,
                    self.product_model.category_id == self.category_model.id,
                )
                .where(self.product_model.sale_date == input_date)
                .group_by(self.category_model.name)
            )
            category_distribution = query.fetchall()
            logger.info(
                f"Category distribution for {input_date}: {category_distribution}"
            )
            return category_distribution
        except Exception as e:
            logger.error(
                f"Error in get_category_distribution_date for {input_date}: {e}"
            )
            raise
