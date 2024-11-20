from typing import Any

from sqlalchemy import RowMapping

from src.domain.entities.base_lxml import (
    BaseLxmlEntity,
    ProductModelWithId,
    CategoryModelWithId,
)
from src.domain.entities.lxml_entities import CategoryEntity


def convert_from_model_to_product_entity_with_id(
    model_dict: dict[Any, Any] | RowMapping[Any, Any]
) -> ProductModelWithId:
    return ProductModelWithId(
        id=model_dict["id"],
        sale_date=model_dict["sale_date"],
        created_at=model_dict["created_at"],
        updated_at=model_dict["updated_at"],
        product=model_dict["product"],
        quantity=model_dict["quantity"],
        price=model_dict["price"],
        category_id=model_dict["category_id"],
    )


def convert_from_model_to_product_entity_without_id(
    model_dict: dict[Any, Any]
) -> BaseLxmlEntity:
    return BaseLxmlEntity(
        sale_date=model_dict["sale_date"],
        product=model_dict["product"],
        quantity=model_dict["quantity"],
        price=model_dict["price"],
        category_name=model_dict["category"],
    )


def convert_from_lxml_parse_entity_to_product_entity_with_id(
    model_dict: dict[Any, Any]
) -> BaseLxmlEntity:
    return BaseLxmlEntity(
        sale_date=model_dict["sale_date"],
        product=model_dict["product"],
        quantity=model_dict["quantity"],
        price=model_dict["price"],
        category_name=model_dict["category_name"],
    )


def convert_from_category_model_to_category_with_id(
    model_dict: dict[Any, Any] | RowMapping[Any, Any]
) -> CategoryModelWithId:
    return CategoryModelWithId(
        id=model_dict["id"],
        name=model_dict["name"],
        created_at=model_dict["created_at"],
        updated_at=model_dict["updated_at"],
    )


def convert_from_category_model_to_category_only_with_name(
    model_dict: dict[Any, Any]
) -> CategoryEntity:
    return CategoryEntity(name=model_dict["name"])


def convert_into_kopeck(to_be_converted: float, constant: int = 100) -> int:
    return int(to_be_converted * constant)
