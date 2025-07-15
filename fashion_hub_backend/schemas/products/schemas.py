from datetime import datetime

from fashion_hub_backend.utils.base_schemas import BaseSchema


class ProductBase(BaseSchema):
    title: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    category_name: str


class ProductCreateWithImage(ProductBase):
    image_path: str


class ProductCreate(ProductBase):
    pass


class Product(ProductCreateWithImage):
    id: int
    created_at: datetime
