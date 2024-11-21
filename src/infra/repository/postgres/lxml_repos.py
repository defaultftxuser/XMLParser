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
from src.common.settings.logger import get_logger
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

logger = get_logger(__name__)


@dataclass(eq=False)
class ProductRepository(PostgresRepo):

    async def get_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            logger.debug(f"Fetching product with ID: {entity.to_dict()}")
            product = await self.get_one(entity=entity.to_dict(), session=session)
            if not product:
                logger.debug(f"No product found for ID: {entity.to_dict()}")
                return None
            logger.debug(f"Product found: {product}")
            return convert_from_model_to_product_entity_with_id(product)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching product with ID {entity.to_dict()}: {e}")
            raise e

    async def get_products(
        self,
        session: AsyncSession,
        entity: ProductEntityWithCategoryId,
        filters: PaginationFilters,
    ) -> list[ProductModelWithId] | None:
        try:
            logger.debug(
                f"Fetching products with filters: {filters} and entity: {entity.to_dict()}"
            )
            products = await self.get_many(
                entity=entity.to_dict(), session=session, filters=filters
            )
            if not products:
                logger.debug(f"No products found for entity: {entity.to_dict()}")
                return None
            logger.debug(f"Found {len(products)} products.")
            return [
                convert_from_model_to_product_entity_with_id(product)
                for product in products
            ]
        except SQLAlchemyError as e:
            logger.error(f"Error fetching products for entity {entity.to_dict()}: {e}")
            raise e

    async def create_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            logger.debug(f"Creating product with data: {entity.to_dict()}")
            query = (
                insert(self.model)
                .values(**entity.to_dict())
                .on_conflict_do_update(
                    index_elements=["product", "category_id"],
                    set_={"quantity": self.model.quantity + entity.quantity.quantity},
                )
            ).returning(self.model.__table__)
            product = await session.execute(query)
            logger.debug(f"Product created/updated: {product}")
            return convert_from_model_to_product_entity_with_id(
                product.mappings().fetchone()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error creating product with data {entity.to_dict()}: {e}")
            raise e

    async def update_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            logger.debug(f"Updating product with data: {entity.to_dict()}")
            product = await self.update_one(entity=entity.to_dict(), session=session)
            if product:
                logger.debug(f"Product updated: {product}")
                return convert_from_model_to_product_entity_with_id(product)
            logger.debug(f"No product found for update: {entity.to_dict()}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error updating product with data {entity.to_dict()}: {e}")
            raise e

    async def delete_product(
        self, session: AsyncSession, entity: ProductEntityWithCategoryId
    ) -> ProductModelWithId | None:
        try:
            logger.debug(f"Deleting product with data: {entity.to_dict()}")
            product = await self.delete_one(entity=entity.to_dict(), session=session)
            if product:
                logger.debug(f"Product deleted: {product}")
                return convert_from_model_to_product_entity_with_id(product)
            logger.debug(f"No product found for deletion: {entity.to_dict()}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error deleting product with data {entity.to_dict()}: {e}")
            raise e


@dataclass(eq=False)
class CategoryRepository(PostgresRepo):

    async def get_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            logger.debug(f"Fetching category with data: {entity.to_dict()}")
            category = await self.get_one(entity=entity.to_dict(), session=session)
            if category:
                logger.debug(f"Category found: {category}")
                return convert_from_category_model_to_category_with_id(category)
            logger.debug(f"No category found for entity: {entity.to_dict()}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error fetching category with data {entity.to_dict()}: {e}")
            raise e

    async def get_categories(
        self, session: AsyncSession, entity: CategoryEntity, filters: PaginationFilters
    ) -> list[CategoryModelWithId] | None:
        try:
            logger.debug(
                f"Fetching categories with filters: {filters} and entity: {entity.to_dict()}"
            )
            categories = await self.get_many(
                entity=entity.to_dict(), session=session, filters=filters
            )
            if not categories:
                logger.debug(f"No categories found for entity: {entity.to_dict()}")
                return None
            logger.debug(f"Found {len(categories)} categories.")
            return [
                convert_from_category_model_to_category_with_id(category)
                for category in categories
            ]
        except SQLAlchemyError as e:
            logger.error(
                f"Error fetching categories for entity {entity.to_dict()}: {e}"
            )
            raise e

    async def create_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            logger.debug(f"Creating category with data: {entity.to_dict()}")
            category = await self.create_one(entity=entity.to_dict(), session=session)
            if category:
                logger.debug(f"Category created: {category}")
                return convert_from_category_model_to_category_with_id(category)
            logger.debug(f"Category not created for data: {entity.to_dict()}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error creating category with data {entity.to_dict()}: {e}")
            raise e

    async def get_or_create(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId:
        try:
            logger.debug(f"Getting or creating category with data: {entity.to_dict()}")
            query = (
                insert(self.model)
                .values(**entity.to_dict())
                .on_conflict_do_update(
                    index_elements=["name"], set_={"updated_at": datetime.now()}
                )
            ).returning(self.model.__table__.c)
            result = await session.execute(query)
            logger.debug(f"Category processed (created or updated): {result}")
            return convert_from_category_model_to_category_with_id(
                result.mappings().fetchone()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error processing category with data {entity.to_dict()}: {e}")
            raise e

    async def update_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            logger.debug(f"Updating category with data: {entity.to_dict()}")
            category = await self.update_one(entity=entity.to_dict(), session=session)
            if category:
                logger.debug(f"Category updated: {category}")
                return convert_from_category_model_to_category_with_id(category)
            logger.debug(f"No category found for update: {entity.to_dict()}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error updating category with data {entity.to_dict()}: {e}")
            raise e

    async def delete_category(
        self, session: AsyncSession, entity: CategoryEntity
    ) -> CategoryModelWithId | None:
        try:
            logger.debug(f"Deleting category with data: {entity.to_dict()}")
            category = await self.delete_one(entity=entity.to_dict(), session=session)
            if category:
                logger.debug(f"Category deleted: {category}")
                return convert_from_category_model_to_category_with_id(category)
            logger.debug(f"No category found for deletion: {entity.to_dict()}")
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error deleting category with data {entity.to_dict()}: {e}")
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
        try:
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

            logger.debug("Executing query: %s", query)  # Log the query at DEBUG level
            result = await session.execute(query)
            products = result.mappings().all()

            logger.debug(
                "Fetched %d products with category", len(products)
            )  # Log the result count at INFO level
            return products

        except Exception as e:
            logger.error(
                "Error occurred while fetching products with category: %s", e
            )  # Log errors at ERROR level
            raise e
