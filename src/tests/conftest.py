import pytest
from faker import Faker


@pytest.fixture()
def get_faker():
    return Faker()
