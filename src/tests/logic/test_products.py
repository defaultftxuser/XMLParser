import datetime

import pytest

from src.domain.entities.base_lxml import ProductEntityWithCategoryId
from src.domain.entities.lxml_entities import (
    CategoryEntity,
    ProductEntity,
    QuantityEntity,
    PriceEntity,
)
from src.infra.repository.postgres.lxml_repos import (
    CategoryRepository,
    ProductRepository,
)


@pytest.mark.asyncio
async def test_create_category_and_product(db_session, get_container):
    product_repo: ProductRepository = get_container.resolve(ProductRepository)
    category_repo: CategoryRepository = get_container.resolve(CategoryRepository)

    category = await category_repo.create_category(
        session=db_session, entity=CategoryEntity(name="Test category")
    )
    category_id = category.id
    product_entity = ProductEntityWithCategoryId(
        category_id=category_id,
        sale_date=datetime.date.today(),
        product=ProductEntity("Test Product"),
        quantity=QuantityEntity(10),
        price=PriceEntity(100),
    )

    result = await product_repo.create_product(
        session=db_session, entity=product_entity
    )
    assert result is not None
    assert result.product == "Test Product"
    assert result.quantity == 10
    assert result.price == 100

    # TODO finish tests
