import uuid
from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    product: str | None
    quantity: str | None
    price: int | None
    category_id: Optional[uuid, str] = ""
