from fashion_hub_backend.utils.base_schemas import BaseSchema


class OrderedItemBase(BaseSchema):
    order_id: int
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderedItem(OrderedItemBase):
    id: int


class OrderedItemCreate(OrderedItemBase):
    pass


class OrderedItemUpdate(BaseSchema):
    quantity: int
    price_at_purchase: float
