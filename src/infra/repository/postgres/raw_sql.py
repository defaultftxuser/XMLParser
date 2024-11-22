from dataclasses import dataclass
from datetime import date
from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.settings.logger import get_logger

logger = get_logger(__name__)


@dataclass(eq=False)
class QueryRepository:
    product_model: Any
    category_model: Any

    async def get_date_total_revenue(self, session: AsyncSession, input_date: date):

        query = select(
            func.sum(self.product_model.price * self.product_model.quantity) / 100
        ).where(self.product_model.sale_date == input_date)
        result = await session.execute(query)
        total_revenue = result.scalar()
        return total_revenue

    async def get_date_top_three_products(
        self, session: AsyncSession, input_date: date
    ):

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
        return top_products

    async def get_category_distribution_date(
        self, session: AsyncSession, input_date: date
    ):
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
        return category_distribution
