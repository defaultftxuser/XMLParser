from dataclasses import dataclass

from src.domain.entities.lxml_entities import ProductEntity, QuantityEntity, PriceEntity, CategoryEntity


@dataclass(eq=False)
class BaseLxmlEntity:
    product: ProductEntity
    quantity: QuantityEntity
    price: PriceEntity
    category: CategoryEntity
