from fastapi import Depends
from sqlalchemy.orm import Session

from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.database.orders import models
from fashion_hub_backend.database.users import models as user_models
from fashion_hub_backend.errors import APINotFound
from fashion_hub_backend.schemas.orders import schemas


class OrderService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def create_order(self, order: schemas.OrderCreate):
        user = self.db.scalars(
            user_models.Users.select().where(user_models.Users.id == order.user_id)
        ).first()
        if not user:
            raise APINotFound(detail=f"User with id: {order.user_id} does not exist")

        order = order.model_dump(exclude_unset=True)
        query = models.Orders.insert().values([order])
        new_order = self.db.scalars(query).first()
        return schemas.Order.model_validate(new_order, from_attributes=True)

    def get_order(self, order_id: int):
        order = self.db.scalars(
            models.Orders.select().where(models.Orders.id == order_id)
        ).first()
        if not order:
            raise APINotFound(detail=f"Order with id: {order_id} does not exist")
        return schemas.Order.model_validate(order, from_attributes=True)

    def get_orders(self):
        orders = self.db.scalars(models.Orders.select()).all()
        if orders is None:
            raise APINotFound(detail="No orders found")
        return [
            schemas.Order.model_validate(order, from_attributes=True)
            for order in orders
        ]

    def update_order(self, order_id: int, order: schemas.OrderUpdate):
        order_exists = self.db.scalars(
            models.Orders.select().where(models.Orders.id == order_id)
        ).first()
        if not order_exists:
            raise APINotFound(detail=f"Order with id: {order_id} does not exist")
        if order.order_status is not None:
            order_exists.order_status = order.order_status
        if order.payment_status is not None:
            order_exists.payment_status = order.payment_status

        return schemas.Order.model_validate(order_exists, from_attributes=True)

    def delete_order(self, order_id: int):
        order = self.db.scalars(
            models.Orders.select().where(models.Orders.id == order_id)
        ).first()
        if order is None:
            raise APINotFound(detail=f"Order with id: {order_id} does not exist")
        self.db.delete(order)
        msg = f"Order with id: {order_id} has been deleted"
        return msg
