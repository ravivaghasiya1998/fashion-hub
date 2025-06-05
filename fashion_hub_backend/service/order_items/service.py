from fastapi import Depends
from sqlalchemy.orm import Session

from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.database.order_items import models
from fashion_hub_backend.database.orders import models as order_models
from fashion_hub_backend.database.products import models as product_models
from fashion_hub_backend.errors import APIBadRequest, APINotFound
from fashion_hub_backend.schemas.order_items import schemas


class OrderItemService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def create_order_item(self, order_item: schemas.OrderedItemCreate):
        order_exists = self.db.scalars(
            order_models.Orders.select().where(
                order_models.Orders.id == order_item.order_id
            )
        ).first()
        if not order_exists:
            raise APIBadRequest(
                detail=f"Order with id: {order_item.order_id} does not exist"
            )
        product_exists = self.db.scalars(
            product_models.Products.select().where(
                product_models.Products.id == order_item.product_id
            )
        ).first()
        if not product_exists:
            raise APIBadRequest(
                detail=f"Product with id: {order_item.product_id} does not exist"
            )

        order_item = order_item.model_dump(exclude_unset=True)
        query = models.OrderedItem.insert().values([order_item])
        new_order_item = self.db.scalars(query).first()
        return schemas.OrderedItem.model_validate(new_order_item, from_attributes=True)

    def get_order_item(self, order_item_id: int):
        order_item = self.db.scalars(
            models.Orders.select().where(models.OrderedItem.id == order_item_id)
        ).first()
        if not order_item:
            raise APINotFound(
                detail=f"Order item with id: {order_item_id} does not exist"
            )
        return schemas.OrderedItem.model_validate(order_item, from_attributes=True)

    def get_order_items(self):
        orders = self.db.scalars(models.OrderedItem.select()).all()
        if orders is None:
            raise APINotFound(detail="No order items found")
        return [
            schemas.OrderedItem.model_validate(order, from_attributes=True)
            for order in orders
        ]

    def update_order_item(
        self, order_item_id: int, order_item: schemas.OrderedItemUpdate
    ):
        order_items_exists = self.db.scalars(
            models.OrderedItem.select().where(models.OrderedItem.id == order_item_id)
        ).first()
        if not order_items_exists:
            raise APINotFound(
                detail=f"Order item with id: {order_item_id} does not exist"
            )
        if order_item.quantity is not None:
            order_items_exists.quantity = order_item.quantity
        if order_item.price_at_purchase is not None:
            order_items_exists.price_at_purchase = order_item.price_at_purchase

        return schemas.OrderedItem.model_validate(
            order_items_exists, from_attributes=True
        )

    def delete_order_item(self, order_item_id: int):
        order_item = self.db.scalars(
            models.OrderedItem.select().where(models.OrderedItem.id == order_item_id)
        ).first()
        if order_item is None:
            raise APINotFound(
                detail=f"Order item with id: {order_item_id} does not exist"
            )
        self.db.delete(order_item)
        msg = f"Order item with id: {order_item_id} has been deleted"
        return msg
