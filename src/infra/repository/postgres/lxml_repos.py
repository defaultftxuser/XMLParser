from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.converters.converters import (
    convert_from_model_to_product_entity_with_id,
    convert_from_category_model_to_category_with_id,
)
from src.common.filters.pagination import PaginationFilters
from src.domain.entities.base_lxml import (
    ProductModelWithId,
    CategoryModelWithId,
    ProductEntityWithCategoryId,
)
from src.domain.entities.lxml_entities import (
    CategoryEntity,
)
from src.infra.db.postgres.models.lxml_models import Product, Category
from src.infra.repository.postgres.base_postgres import PostgresRepo


@dataclass(eq=False)
class ProductRepository(PostgresRepo):

    async def get_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            product = await self.get_one(entity=entity.to_dict(), session=session)
            if not product:
                return None
            return convert_from_model_to_product_entity_with_id(product)
        except SQLAlchemyError as e:
            raise e

    async def get_products(
        self,
        session: AsyncSession,
        entity: ProductEntityWithCategoryId,
        filters: PaginationFilters,
    ) -> list[ProductModelWithId] | None:
        try:
            products = await self.get_many(
                entity=entity.to_dict(), session=session, filters=filters
            )
            if not products:
                return None
            return [
                convert_from_model_to_product_entity_with_id(product)
                for product in products
            ]
        except SQLAlchemyError as e:
            raise e

    async def create_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            query = (
                insert(self.model)
                .values(**entity.to_dict())
                .on_conflict_do_update(
                    index_elements=["product", "category_id"],
                    set_={"quantity": self.model.quantity + entity.quantity.quantity},
                )
            ).returning(self.model.__table__)
            product = await session.execute(query)
            return convert_from_model_to_product_entity_with_id(
                product.mappings().fetchone()
            )
        except SQLAlchemyError as e:
            raise e

    async def update_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            product = await self.update_one(entity=entity.to_dict(), session=session)
            return (
                convert_from_model_to_product_entity_with_id(product)
                if product
                else None
            )
        except SQLAlchemyError as e:
            raise e

    async def delete_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            product = await self.delete_one(entity=entity.to_dict(), session=session)
            return (
                convert_from_model_to_product_entity_with_id(product)
                if product
                else None
            )
        except SQLAlchemyError as e:
            raise e


@dataclass(eq=False)
class CategoryRepository(PostgresRepo):

    async def get_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            category = await self.get_one(entity=entity.to_dict(), session=session)
            if category:
                return convert_from_category_model_to_category_with_id(category)
            return None
        except SQLAlchemyError as e:
            raise e

    async def get_categories(
        self, session: AsyncSession, entity: CategoryEntity, filters: PaginationFilters
    ) -> list[CategoryModelWithId] | None:
        try:
            categories = await self.get_many(
                entity=entity.to_dict(), session=session, filters=filters
            )
            if not categories:
                return None
            return [
                convert_from_category_model_to_category_with_id(category)
                for category in categories
            ]
        except SQLAlchemyError as e:
            raise e

    async def create_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:

            category = await self.create_one(entity=entity.to_dict(), session=session)
            return (
                convert_from_category_model_to_category_with_id(category)
                if category
                else None
            )
        except SQLAlchemyError as e:
            raise e

    async def get_or_create(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId:

        query = (
            (insert(self.model).values(**entity.to_dict())).on_conflict_do_update(
                index_elements=["name"], set_={"updated_at": datetime.now()}
            )
        ).returning(self.model.__table__.c)
        result = await session.execute(query)
        return convert_from_category_model_to_category_with_id(
            result.mappings().fetchone()
        )

    async def update_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            category = await self.update_one(entity=entity.to_dict(), session=session)
            return (
                convert_from_category_model_to_category_with_id(category)
                if category
                else None
            )
        except SQLAlchemyError as e:
            raise e

    async def delete_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            category = await self.delete_one(entity=entity.to_dict(), session=session)
            return (
                convert_from_category_model_to_category_with_id(category)
                if category
                else None
            )
        except SQLAlchemyError as e:
            raise e


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
        return result.mappings().all()
