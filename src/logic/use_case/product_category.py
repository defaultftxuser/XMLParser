import asyncio
from dataclasses import dataclass

from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import (
    BaseLxmlEntity,
)

from src.infra.exceptions.exceptions import SQLException

from src.logic.repo_service.product_category_service import ProductCategoryService
from src.logic.xml_parser import LXMLParser


logger = get_logger(__name__)


@dataclass(eq=False)
class CreateProductCategoryUseCase:
    service: ProductCategoryService

    async def create_product_category_usecase(self, entity: BaseLxmlEntity):
        try:
            product = await self.service.create_category_product(entity=entity)
            return product
        except SQLException as e:
            logger.error(f"SQL error while creating product or category: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while processing entity {entity}: {e}")
            raise


@dataclass(eq=False)
class ParseAndCreateProductCategoryUseCase:
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
