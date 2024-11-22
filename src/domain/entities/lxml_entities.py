import uuid
from dataclasses import dataclass, field
from typing import Optional

from src.domain.entities.base import BaseEntity
from src.domain.exceptions.entities import (
    ProductLengthTooLongException,
    ProductLengthTooShortException,
    TooSmallQuantityException,
    TooSmallPriceException,
)


@dataclass(eq=False)
class ProductEntity(BaseEntity):
    name: str

    def validate(self):
        if len(self.name) < 1:
            raise ProductLengthTooShortException(self.name)

        if len(self.name) > 100:
            raise ProductLengthTooLongException(self.name)

    def to_dict(self):
        return {"name": self.name}


@dataclass(eq=False)
class ProductIdEntity(BaseEntity):
    product_id: Optional[uuid] = field(default_factory=uuid.uuid4)

    def validate(self): ...

    def to_dict(self):
        return {"product_id": self.product_id}


@dataclass(eq=False)
class QuantityEntity(BaseEntity):
    quantity: int

    def validate(self):
        if self.quantity <= 0:
            raise TooSmallQuantityException(self.quantity)

    def to_dict(self):
        return {"name": self.quantity}


@dataclass(eq=False)
class PriceEntity(BaseEntity):
    price: int

    def validate(self):
        if self.price < 0:
            raise TooSmallPriceException(self.price)

    def to_dict(self):
        return {"name": self.price}


@dataclass(eq=False)
class CategoryEntity(BaseEntity):
    name: str | None = ""

    def validate(self): ...

    def to_dict(self):
        return {"name": self.name}


@dataclass(eq=False)
class CategoryQuery(BaseEntity):
    name: str | None = ""

    def validate(self): ...

    def to_dict(self):
        if not self.name:
            return
        return {"name": self.name}
