import uuid
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Any

import bson

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
    category_name: str

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
            key: value
            for key, value in {
                "id": self.id,
                "sale_date": self.sale_date,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "product": self.product,
                "quantity": self.quantity,
                "price": self.price,
                "category_id": self.category_id,
            }.items()
            if value is not None
        }


@dataclass(eq=False)
class ProductEntityWithCategoryId(BaseEntity):
    category_id: uuid
    sale_date: date
    product: ProductEntity
    quantity: QuantityEntity
    price: PriceEntity

    def __post_init__(self):
        self.validate()

    def validate(self): ...

    def to_dict(self):

        return {
            "product": self.product.name,
            "sale_date": self.sale_date,
            "quantity": self.quantity.quantity,
            "price": self.price.price,
            "category_id": self.category_id,
        }


@dataclass(eq=False)
class ProductEntityWithoutCategoryId(BaseEntity):
    sale_date: date
    product: ProductEntity
    quantity: QuantityEntity
    price: PriceEntity

    def __post_init__(self):
        self.validate()

    def validate(self): ...

    def to_dict(self):

        return {
            "product": self.product.name,
            "sale_date": self.sale_date,
            "quantity": self.quantity.quantity,
            "price": self.price.price,
        }


@dataclass(eq=False)
class ProductQuery(BaseEntity):
    sale_date: date | None = field(default=None)
    product: str | None = field(default=None)
    quantity: int | None = field(default=None)
    price: int | None = field(default=None)
    category_id: Optional[uuid] = field(default=None)

    def __post_init__(self):
        self.validate()

    def validate(self): ...

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in {
                "product": self.product,
                "sale_date": self.sale_date,
                "quantity": self.quantity,
                "price": self.price,
                "category_id": self.category_id,
            }.items()
            if value is not None
        }


@dataclass(eq=False)
class CategoryModelWithId(BaseEntity, BaseModelEntity):
    name: str

    def validate(self): ...

    def to_dict(self):
        return {
            key: value
            for key, value in {
                "id": self.id,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "name": self.name,
            }.items()
            if value is not None
        }


@dataclass(eq=False)
class GPTAnswerEntity(BaseEntity):
    sale_date: str | date
    answer: str

    def validate(self):
        if not isinstance(self.sale_date, str):
            self.sale_date = str(self.sale_date)

    def to_dict(self):
        return {"sale_date": self.sale_date, "answer": self.answer}


@dataclass(eq=False)
class GPTAnswerModel(BaseEntity):
    sale_date: str
    answer: str
    _id: bson

    def validate(self):
        if not isinstance(self.sale_date, str):
            self.sale_date = str(self.sale_date)

    def to_dict(self):
        return {"_id": self._id, "sale_date": self.sale_date, "answer": self.answer}
