from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import AbstractModel


class Category(AbstractModel):
    __tablename__ = 'categories'

    name = Column(String, nullable=False)

    products = relationship('Product', back_populates='category')


class Product(AbstractModel):
    __tablename__ = 'products'

    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)

    category = relationship('Category', back_populates='products')
