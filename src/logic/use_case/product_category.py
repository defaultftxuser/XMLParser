import asyncio
from dataclasses import dataclass

from src.common.settings.config import get_settings
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    BaseLxmlEntity,
    ProductEntityWithCategoryId,
)
from src.domain.entities.lxml_entities import (
    CategoryEntity,
)
from src.infra.db.postgres.db import AsyncPostgresClient
from src.infra.db.postgres.models.lxml_models import Category, Product
from src.infra.exceptions.exceptions import SQLException
from src.infra.repository.postgres.lxml_repos import (
    CategoryRepository,
    ProductRepository,
)
from src.logic.repo_service.category_service import CategoryService
from src.logic.repo_service.product_service import ProductService
from src.logic.xml_parser import LXMLParser


logger = get_logger(__name__)


@dataclass(eq=False)
class CreateProductCategoryUseCase:
    category_service: CategoryService
    product_service: ProductService
    uow: AsyncPostgresClient

    async def create_product_category_usecase(self, entity: BaseLxmlEntity):
        async with self.uow.get_async_session() as session:  # noqa
            try:
                logger.debug(f"Starting to process entity: {entity}")
                category = await self.category_service.create_category(
                    entity=CategoryEntity(name=entity.category_name),
                    session=session,
                )
                logger.info(f"Category created: {category}")

                product = await self.product_service.create_product(
                    entity=ProductEntityWithCategoryId(
                        product=entity.product,
                        sale_date=entity.sale_date,
                        quantity=entity.quantity,
                        price=entity.price,
                        category_id=category.id,
                    ),
                    session=session,
                )
                logger.info(f"Product created: {product}")
                return product
            except SQLException as e:
                logger.error(
                    f"SQL error while creating product or category: {e.message}"
                )
                raise
            except Exception as e:
                logger.error(f"Unexpected error while processing entity {entity}: {e}")
                raise


@dataclass(eq=False)
class ParseAndCreateProductCategoryUseCase(CreateProductCategoryUseCase):
    category_service: CategoryService
    product_service: ProductService
    uow: AsyncPostgresClient
    parser: LXMLParser

    async def parse_and_create(self, lxml_data: str, element: str = "//product"):
        try:
            entities: list[BaseLxmlEntity] | None = self.parser.parsing(
                lxml_data=lxml_data, element=element
            )
            if len(entities) > 0:
                batch = []
                for entity in entities:
                    batch.append(self.create_product_category_usecase(entity=entity))
                    if len(batch) == 100:
                        await asyncio.gather(*batch)
                if len(batch) > 0:
                    await asyncio.gather(*batch)
                    return (
                        f"products {len(entities)=} succesfully created",
                        entity.sale_date,
                    )
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing data: {e}")
            return f"Error occurred while parsing XML: {e}", None
        except Exception as e:
            logger.error(f"Unexpected error during parse and create operation: {e}")
            return f"Unexpected error: {e}", None


def get_product_service_usecase():
    return CreateProductCategoryUseCase(
        category_service=CategoryService(repository=CategoryRepository(model=Category)),
        product_service=ProductService(repository=ProductRepository(model=Product)),
        uow=AsyncPostgresClient(settings=get_settings()),
    )


def get_parse_and_create_products():
    return ParseAndCreateProductCategoryUseCase(
        category_service=CategoryService(repository=CategoryRepository(model=Category)),
        product_service=ProductService(repository=ProductRepository(model=Product)),
        uow=AsyncPostgresClient(settings=get_settings()),
        parser=LXMLParser(),
    )
