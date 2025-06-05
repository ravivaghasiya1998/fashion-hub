from datetime import datetime
from enum import auto

from strenum import StrEnum

from fashion_hub_backend.utils.base_schemas import BaseSchema
from fashion_hub_backend.utils.enums import OrderStatus,PaymentStatus 





class OrderBase(BaseSchema):
    user_id: int
    order_amount: float
    order_status: OrderStatus
    payment_status: PaymentStatus
    ordered_at: datetime


class Order(OrderBase):
    id: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseSchema):
    order_status: OrderStatus
    payment_status: PaymentStatus
