
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Float, Integer

from fashion_hub_backend.database.db_setup import Base
from fashion_hub_backend.database.orders.models import Orders

# from fashion_hub_backend.database.products.models import Products


class OrderedItem(Base):
    __tablename__ = "ordered_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    price_at_purchase: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["Orders"] = relationship(
        "Orders",
        back_populates="order_items",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    # Relationship with Products table
    product: Mapped["Products"] = relationship(
        "Products",
        back_populates="order_items",  # Products will have a reciprocal relationship here
    )
    