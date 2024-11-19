from dataclasses import dataclass, field


@dataclass(eq=False)
class ProductEntity:
    name: str


@dataclass(eq=False)
class QuantityEntity:
    quantity: int


@dataclass(eq=False)
class PriceEntity:
    price: str


@dataclass(eq=False)
class CategoryEntity:
    category: str
