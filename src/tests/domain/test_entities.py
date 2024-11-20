import pytest

from src.domain.entities.lxml_entities import (
    ProductEntity,
    QuantityEntity,
    PriceEntity,
    CategoryEntity,
    ProductIdEntity,
)
from src.domain.exceptions.entities import (
    ProductLengthTooShortException,
    ProductLengthTooLongException,
    TooSmallQuantityException,
    TooSmallPriceException,
)


@pytest.mark.asyncio
async def test_product_creation():
    product = ProductEntity(name="Some product")

    assert product.name == "Some product"


@pytest.mark.asyncio
async def test_product_creation_too_short():
    with pytest.raises(ProductLengthTooShortException):
        ProductEntity(name="")


@pytest.mark.asyncio
async def test_product_creation_too_long():
    with pytest.raises(ProductLengthTooLongException):
        ProductEntity(name="a" * 200)


@pytest.mark.asyncio
async def test_quantity_creation():
    quantity = QuantityEntity(quantity=5)
    assert quantity.quantity == 5


@pytest.mark.asyncio
async def test_quantity_creation_too_small():
    with pytest.raises(TooSmallQuantityException):
        QuantityEntity(quantity=0)


@pytest.mark.asyncio
async def test_quantity_creation():
    quantity = QuantityEntity(quantity=5)
    assert quantity.quantity == 5


@pytest.mark.asyncio
async def test_price_creation():
    price = PriceEntity(price=225)
    assert price.price == 225


@pytest.mark.asyncio
async def test_price_creation():
    with pytest.raises(TooSmallPriceException):
        PriceEntity(price=-1)


@pytest.mark.asyncio
async def test_category_creation():
    category = CategoryEntity(name="")
    assert category.name == ""


@pytest.mark.asyncio
async def test_product_id_creation():
    category = ProductIdEntity(product_id=123)
    assert category.product_id == 123
