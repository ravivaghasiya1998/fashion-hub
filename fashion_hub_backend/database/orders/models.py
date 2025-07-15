from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Float, Integer

from fashion_hub_backend.database.db_setup import Base
from fashion_hub_backend.database.users.models import Users

# from fashion_hub_backend.database.payments.models import Payment
from fashion_hub_backend.schemas.orders.schemas import OrderStatus, PaymentStatus

# from fashion_hub_backend.database.order_items.models import OrderedItem


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    order_amount: Mapped[float] = mapped_column(Float, nullable=False)
    order_status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    payment_status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    ordered_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="orders")

    order_items: Mapped[list["OrderedItem"]] = relationship(
        "OrderedItem", back_populates="order", cascade="all, delete-orphan"
    )
    payment: Mapped["Payment"] = relationship("Payment", back_populates="order", cascade="all,delete-orphan")
