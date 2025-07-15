from fastapi import APIRouter, Depends, status

from fashion_hub_backend.schemas.payments import schemas
from fashion_hub_backend.service.payments.service import PaymentService

payment_router = APIRouter(prefix="/v1", tags=["payment"])  # , dependencies=[Depends(get_current_active_user)])


@payment_router.post("/payments", status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: schemas.PaymentCreate, service: PaymentService = Depends(PaymentService)
) -> schemas.Payment:
    payment = service.create_payment(payment)
    service.commit()
    return payment


@payment_router.get("/payments")
def get_payments(service: PaymentService = Depends(PaymentService)) -> list[schemas.Payment]:
    payments = service.get_payments()
    return payments


@payment_router.get("/payments/{payment_id}")
def get_payment(payment_id: int, service: PaymentService = Depends(PaymentService)) -> schemas.Payment:
    order = service.get_payment(payment_id)
    return order


@payment_router.put("/payments/{payment_id}")
def update_payment(
    payment_id: int,
    payment: schemas.PaymentCreate,
    service: PaymentService = Depends(PaymentService),
) -> schemas.Payment:
    payment = service.update_payment(payment_id, payment)
    service.commit()
    return payment


@payment_router.delete("/payments/{opayment_id}")
def delete_payment(payment_id: int, service: PaymentService = Depends(PaymentService)):
    msg = service.delete_payment(payment_id)
    service.commit()
    return msg
