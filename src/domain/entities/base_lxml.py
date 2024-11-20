import uuid
from dataclasses import dataclass
from datetime import datetime, date

from src.domain.entities.base import BaseEntity
from src.domain.entities.lxml_entities import (
    ProductEntity,
    QuantityEntity,
    PriceEntity,
    ProductIdEntity,
)


@dataclass(eq=False)
class BaseModelEntity:
    id: uuid
    created_at: datetime
    updated_at: datetime


@dataclass(eq=False)
class BaseLxmlEntity(BaseEntity):
    product: ProductEntity
    sale_date: date
    quantity: QuantityEntity
    price: PriceEntity
    category_name: str = ""

    def __post_init__(self):
        self.validate()

    def validate(self): ...

    def to_dict(self):
        return {
            "product": self.product,
            "quantity": self.quantity,
            "price": self.price,
            "category_name": self.category_name,
            "sale_date": self.sale_date,
        }


@dataclass(eq=False)
class ProductModelWithId(BaseEntity, BaseModelEntity):
    sale_date: date
    product: ProductEntity
    quantity: QuantityEntity
    price: PriceEntity
    category_id: ProductIdEntity | None = None

    def __post_init__(self):
        self.validate()

    def validate(self): ...

    def to_dict(self):
        return {
            "id": self.id,
            "sale_date": self.sale_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "product": self.product,
            "quantity": self.quantity,
            "price": self.price,
            "category_id": self.category_id,
        }


@dataclass(eq=False)
class ProductEntityWithCategoryId(BaseEntity):
    category_id: uuid
    product: ProductEntity
    quantity: QuantityEntity
    price: PriceEntity

    def __post_init__(self):
        self.validate()

    def validate(self): ...

    def to_dict(self):

        return {
            "product": self.product.name,
            "quantity": self.quantity.quantity,
            "price": self.price.price,
            "category_id": self.category_id,
        }


@dataclass(eq=False)
class CategoryModelWithId(BaseEntity, BaseModelEntity):
    name: str

    def validate(self): ...

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "name": self.name,
        }
