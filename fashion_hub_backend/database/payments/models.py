from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as POSTGRESQLUUID

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Float, Integer, String
from sqlalchemy import Enum as SQLEnum
from fashion_hub_backend.database.orders.models import Orders

from fashion_hub_backend.database.db_setup import Base
from fashion_hub_backend.utils.enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(SQLEnum(PaymentMethod), nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus), default=PaymentStatus.PENDING
    )
    transaction_id: Mapped[UUID] = mapped_column(POSTGRESQLUUID(as_uuid=True), nullable=False)

    paid_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    
    order: Mapped["Orders"] = relationship("Orders", back_populates="payment")


    user: Mapped["Users"] = relationship("Users", back_populates="payment")
