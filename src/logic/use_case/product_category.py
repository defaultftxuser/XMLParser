import asyncio
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    BaseLxmlEntity,
    ProductEntityWithCategoryId,
)
from src.domain.entities.lxml_entities import (
    CategoryEntity,
)

from src.infra.exceptions.exceptions import SQLException


from src.logic.repo_service.category_service import CategoryService
from src.logic.repo_service.product_service import ProductService
from src.logic.xml_parser import LXMLParser


logger = get_logger(__name__)


@dataclass(eq=False)
class CreateProductCategoryUseCase:
    category_service: CategoryService
    product_service: ProductService
    session: AsyncSession

    async def create_product_category_usecase(self, entity: BaseLxmlEntity):
        async with self.session() as session:  # noqa
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
class ParseAndCreateProductCategoryUseCase:
    category_service: CategoryService
    product_service: ProductService
    parser: LXMLParser
    product_service_usecase: CreateProductCategoryUseCase

    async def parse_and_create(self, lxml_data: str, element: str = "//product"):
        try:
            entities: list[BaseLxmlEntity] | None = self.parser.parsing(
                lxml_data=lxml_data, element=element
            )
            if len(entities) > 0:
                batch = []
                for entity in entities:
                    batch.append(
                        self.product_service_usecase.create_product_category_usecase(
                            entity=entity
                        )
                    )
                    if len(batch) == 100:
                        await asyncio.gather(*batch)
                if len(batch) > 0:
                    await asyncio.gather(*batch)
                    return (
                        f"products {len(entities)=} succesfully created",
                        entity.sale_date,
                    )
            return
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing data: {e}")
            return f"Error occurred while parsing XML: {e}", None
        except Exception as e:
            logger.error(f"Unexpected error during parse and create operation: {e}")
            return f"Unexpected error: {e}", None
