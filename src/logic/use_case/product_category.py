import asyncio
from dataclasses import dataclass
import datetime

from src.common.settings.config import get_settings
from src.domain.entities.base_lxml import (
    BaseLxmlEntity,
    ProductEntityWithCategoryId,
)
from src.domain.entities.lxml_entities import (
    CategoryEntity,
    ProductEntity,
    QuantityEntity,
    PriceEntity,
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


@dataclass(eq=False)
class CreateProductCategoryUseCase:
    category_service: CategoryService
    product_service: ProductService
    uow: AsyncPostgresClient

    async def create_product_category_usecase(self, entity: BaseLxmlEntity):
        async with self.uow.get_async_session() as session:  # noqa
            try:
                category = await self.category_service.create_category(
                    entity=CategoryEntity(name=entity.category_name),
                    session=session,
                )
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
                return product
            except SQLException as e:
                raise e.message


@dataclass(eq=False)
class ParseAndCreateProductCategoryUseCase(CreateProductCategoryUseCase):
    category_service: CategoryService
    product_service: ProductService
    uow: AsyncPostgresClient
    parser: LXMLParser

    async def parse_and_create(self, lxml_data: str, element: str = "//product"):
        entities = self.parser.parsing(lxml_data=lxml_data, element=element)
        try:
            if entities:
                batch = []
                for entity in entities:
                    batch.append(self.create_product_category_usecase(entity=entity))
                    if len(batch) == 100:
                        await asyncio.gather(*batch)
                if len(batch) > 0:
                    await asyncio.gather(*batch)
            return
        except Exception as e:
            raise e


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


async def main():
    a = BaseLxmlEntity(
        product=ProductEntity(name="Product R"),
        sale_date=datetime.date(2024, 11, 21),
        quantity=QuantityEntity(quantity=46),
        price=PriceEntity(price=1500),
        category_name="test",
    )
    await get_product_service_usecase().create_product_category_usecase(entity=a)


print(asyncio.run(main()))
