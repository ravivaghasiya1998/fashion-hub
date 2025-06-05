
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Float, Integer, String, Text

from fashion_hub_backend.database.db_setup import Base
from fashion_hub_backend.database.order_items.models import OrderedItem


class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    image_path: Mapped[str] = mapped_column(String, nullable=False)

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    category_name: Mapped[str] = mapped_column(
        String,
        ForeignKey("categories.name", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship with OrderItems table
    order_items: Mapped[list["OrderedItem"]] = relationship(
        "OrderedItem", back_populates="product", cascade="all, delete-orphan"
    )
