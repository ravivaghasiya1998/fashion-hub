from fashion_hub_backend.utils.base_schemas import BaseSchema
from fashion_hub_backend.utils.enums import CategoryName


class CategoryBase(BaseSchema):
    name: CategoryName
    description: str


class Category(CategoryBase):
    id: int


class CategoryCreate(CategoryBase):
    pass
