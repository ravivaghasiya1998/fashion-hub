from fastapi import Depends
from sqlalchemy.orm import Session

from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.database.payments import models
from fashion_hub_backend.database.orders import models as order_models
from fashion_hub_backend.database.users import models as user_models
from fashion_hub_backend.errors import APINotFound
from fashion_hub_backend.schemas.payments import schemas


class PaymentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def create_payment(self, payment: schemas.PaymentCreate):
        order = self.db.scalars(
            order_models.Orders.select().where(order_models.Orders.id == payment.order_id)
        ).first()
        if not order:
            raise APINotFound(key=f"{payment.order_id}",detail=f"Order with id: {payment.order_id} does not exist")
        
        user = self.db.scalars(
            user_models.Users.select().where(user_models.Users.id == payment.user_id)
        ).first()

        if not user:
               raise APINotFound(key=f"{payment.user_id}", detail=f"User with id: {payment.user_id} does not exist")

        payment = payment.model_dump(exclude_unset=True)
        query = models.Payment.insert().values([payment])
        new_payment = self.db.scalars(query).first()
        return schemas.Payment.model_validate(new_payment, from_attributes=True)

    def get_payment(self, payment_id: int):
        payment = self.db.scalars(
            models.Payment.select().where(models.Payment.id == payment_id)
        ).first()
        if not payment:
            raise APINotFound(detail=f"Payment with id: {payment_id} does not exist")
        return schemas.Payment.model_validate(payment, from_attributes=True)

    def get_payments(self):
        payments = self.db.scalars(models.Payment.select()).all()
        if payments is None:
            raise APINotFound(detail="No payments found")
        return [
            schemas.Payment.model_validate(payment, from_attributes=True)
            for payment in payments
        ]

    def update_payment(self, payment_id: int, payment: schemas.PaymentUpdate):
        payment_exists = self.db.scalars(
            models.Payment.select().where(models.Payment.id == payment_id)
        ).first()
        if not payment_exists:
            raise APINotFound(detail=f"Payment with id: {payment_id} does not exist")
        if payment.payment_method is not None:
            payment_exists.payment_method = payment.payment_method
        if payment.payment_status is not None:
            payment_exists.payment_status = payment.payment_status

        return schemas.Payment.model_validate(payment_exists, from_attributes=True)

    def delete_payment(self, payments_id: int):
        payment = self.db.scalars(
            models.Payment.select().where(models.Payment.id == payments_id)
        ).first()
        if payment is None:
            raise APINotFound(detail=f"payment with id: {payments_id} does not exist")
        self.db.delete(payment)
        msg = f"Payment with id: {payments_id} has been deleted"
        return msg
