from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.converters.converters import (
    convert_from_model_to_product_entity_with_id,
    convert_from_category_model_to_category_with_id,
)
from src.common.filters.pagination import PaginationFilters
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    ProductModelWithId,
    CategoryModelWithId,
    ProductEntityWithCategoryId,
    BaseLxmlEntity,
    ProductQuery,
    ProductEntityWithoutCategoryId,
)
from src.domain.entities.lxml_entities import (
    CategoryEntity,
    CategoryQuery,
)
from src.infra.db.postgres.models.lxml_models import Product, Category
from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.base_postgres import PostgresRepo

logger = get_logger(__name__)


@dataclass(eq=False)
class ProductRepository(PostgresRepo):

    async def get(
        self,
        session: AsyncSession,
        entity: ProductQuery,
        limit: int = 10,
        offset: int = 0,
    ) -> list[ProductModelWithId] | None:
        products = await session.execute(
            select(self.model.__table__.columns)
            .filter_by(**entity.to_dict())
            .offset(offset)
            .limit(limit)
        )

        return [
            convert_from_model_to_product_entity_with_id(product)
            for product in products.mappings().all()
        ]

    async def create_one(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:

        query = await session.execute(
            insert(self.model)
            .values(**entity.to_dict())
            .returning(self.model.__table__.columns)
        )

        return convert_from_model_to_product_entity_with_id(query.mappings().fetchone())

    async def create_or_update(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ):
        try:
            created = await self.create_one(session=session, entity=entity)
            return created
        except IntegrityError:
            await session.rollback()
            updated = await self.update_one(
                session=session,
                entity=ProductEntityWithoutCategoryId(
                    sale_date=entity.sale_date,
                    product=entity.product,
                    quantity=entity.quantity,
                    price=entity.price,
                ),
                change_entity=ProductEntityWithoutCategoryId(
                    sale_date=entity.sale_date,
                    product=entity.product,
                    quantity=entity.quantity,
                    price=entity.price,
                ),
            )
            return updated

    async def update_one(
        self,
        session: AsyncSession,
        entity: ProductEntityWithoutCategoryId,
        change_entity: ProductEntityWithoutCategoryId,
    ) -> ProductModelWithId | None:
        updated_model = await session.execute(
            update(self.model)
            .where(
                self.model.product == entity.product.name,
                self.model.sale_date == entity.sale_date,
            )
            .values(quantity=self.model.quantity + entity.quantity.quantity)
            .returning(self.model.__table__.columns)
        )
        return convert_from_model_to_product_entity_with_id(
            updated_model.mappings().fetchone()
        )

    async def delete_one(
        self, session: AsyncSession, entity: ProductQuery
    ) -> ProductModelWithId | None:
        query = await session.execute(
            delete(self.model)
            .filter_by(**entity.to_dict())
            .returning(self.model.__table__.columns)
        )
        return convert_from_model_to_product_entity_with_id(query.mappings().fetchone())


@dataclass(eq=False)
class CategoryRepository(PostgresRepo):

    async def get(
        self,
        session: AsyncSession,
        entity: CategoryQuery,
        limit: int | None = 10,
        offset: int | None = 0,
    ) -> list[CategoryModelWithId] | None:
        products = await session.execute(
            select(self.model.__table__.columns)
            .filter_by(**entity.to_dict())
            .offset(offset)
            .limit(limit)
        )

        return [
            convert_from_category_model_to_category_with_id(product)
            for product in products.mappings().all()
        ]

    async def create_one(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        query = await session.execute(
            insert(self.model)
            .values(**entity.to_dict())
            .returning(self.model.__table__.columns)
        )

        return convert_from_category_model_to_category_with_id(
            query.mappings().fetchone()
        )

    async def update_one(
        self,
        session: AsyncSession,
        entity: CategoryEntity,
        change_entity: CategoryEntity,
    ) -> CategoryModelWithId | None:
        query = (
            update(self.model)
            .filter_by(**entity.to_dict())
            .values(change_entity.to_dict())
            .returning(self.model.__table__.columns)
        )
        result = await session.execute(query)
        return convert_from_category_model_to_category_with_id(
            result.mappings().fetchone()
        )

    async def create_or_update(
        self,
        session: AsyncSession,
        entity: CategoryEntity,
    ) -> CategoryModelWithId | None:
        try:
            inserted = await self.create_one(session=session, entity=entity)
            return inserted
        except IntegrityError:
            await session.rollback()
            return await self.update_one(
                session=session, entity=entity, change_entity=entity
            )

    async def delete_one(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        deleted_product = await session.execute(
            delete(self.model)
            .filter_by(**entity.to_dict())
            .returning(self.model.__table__.columns)
        )
        return convert_from_category_model_to_category_with_id(
            deleted_product.mappings().fetchone()
        )


@dataclass(eq=False)
class ProductCategoryRepository:
    product_repository: ProductRepository
    category_repository: CategoryRepository

    async def get_products_with_category(
        self,
        session,
        entity: dict[Any, Any] | None,
        filters: PaginationFilters | None,
    ):
        query = (
            select(
                self.product_repository.model.product,
                self.product_repository.model.sale_date,
                self.product_repository.model.price,
                self.product_repository.model.quantity,
                self.product_repository.model.created_at,
                self.category_repository.model.name.label("category_name"),
            )
            .filter_by(**entity)
            .join(Category, Product.category_id == Category.id)  # noqa
            .offset(filters.offset)
            .limit(filters.limit)
        )

        result = await session.execute(query)
        products = result.mappings().all()

        return products

    async def create_category_and_product(
        self,
        session,
        entity: BaseLxmlEntity,
    ):
        try:
            category = await self.category_repository.create_or_update(
                session=session, entity=CategoryEntity(name=entity.category_name)
            )
            product = await self.product_repository.create_or_update(
                session=session,
                entity=ProductEntityWithCategoryId(
                    category_id=category.id,
                    sale_date=entity.sale_date,
                    product=entity.product,
                    quantity=entity.quantity,
                    price=entity.price,
                ),
            )
            return product

        except SQLException as e:
            raise e.message
