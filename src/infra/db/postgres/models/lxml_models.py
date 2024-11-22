from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import AbstractModel


class Category(AbstractModel):
    __tablename__ = "categories"

    name = Column(String, nullable=False, unique=True)

    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )


class Product(AbstractModel):
    __tablename__ = "products"
    sale_date = Column(Date, nullable=False)
    product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )

    category = relationship("Category", back_populates="products")

    __table_args__ = (
        UniqueConstraint(
            "product", "category_id", "sale_date", name="uq_product_category_date"
        ),
    )
