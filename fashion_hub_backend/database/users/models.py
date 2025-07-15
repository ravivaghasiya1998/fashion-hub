from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Boolean, DateTime, Integer, String

from fashion_hub_backend.database.db_setup import Base

# from fashion_hub_backend.database.orders.models import Orders


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[dict] = mapped_column(JSONB, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="user")
    payment: Mapped[list["Payment"]] = relationship("Payment", back_populates="user")
