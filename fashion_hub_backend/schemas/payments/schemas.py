from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fashion_hub_backend.utils.base_schemas import BaseSchema
from fashion_hub_backend.utils.enums import PaymentMethod, PaymentStatus


class PaymentBase(BaseSchema):
    order_id: int
    user_id: int
    transaction_id: UUID = uuid4()
    payment_method: PaymentMethod
    payment_status: PaymentStatus


class Payment(PaymentBase):
    paid_at: datetime
    id: int


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseSchema):
    payment_method: Optional[PaymentMethod] = None
    payment_status: Optional[PaymentStatus] = None
