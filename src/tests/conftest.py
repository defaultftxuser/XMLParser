import pytest
from faker import Faker

from src.domain.entities.base_lxml import BaseLxmlEntity
from src.domain.entities.lxml_entities import (
    ProductEntity,
    PriceEntity,
    QuantityEntity,
    CategoryEntity,
)
from src.infra.db.memory.memory_db import InMemoryDatabase


@pytest.fixture()
def get_faker():
    return Faker()


@pytest.fixture()
def fill_database(get_faker):
    database = InMemoryDatabase()
    entities = []
    for _ in range(10):
        product = ProductEntity(name=get_faker.word())
        quantity = QuantityEntity(quantity=get_faker.random_int(min=1, max=100))
        price = PriceEntity(price=round(get_faker.random_number(digits=2), 2))
        category = category = get_faker.word()
        entity = BaseLxmlEntity(
            product=product, quantity=quantity, price=price, category_name=category
        )
        database.add_entity(entity)
    return entities
