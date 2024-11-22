import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.common.filters.pagination import PaginationFilters


class ProductSchema(BaseModel):
    product: str | None
    quantity: str | None
    price: int | None
    category_id: bytes | str = ""


class XMLSchema(BaseModel):
    url: str


class GPTSchemaIn(BaseModel):
    _id: str
    sale_date: Optional[date]
    filters: PaginationFilters
