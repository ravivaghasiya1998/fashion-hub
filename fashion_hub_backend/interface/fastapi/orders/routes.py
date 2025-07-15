from fastapi import APIRouter, Depends, status

from fashion_hub_backend.schemas.orders import schemas
from fashion_hub_backend.service.orders.service import OrderService
from fashion_hub_backend.utils.oauth2 import get_current_active_user

order_router = APIRouter(prefix="/v1", tags=["orders"], dependencies=[Depends(get_current_active_user)])


@order_router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, service: OrderService = Depends(OrderService)) -> schemas.Order:
    order = service.create_order(order)
    service.commit()
    return order


@order_router.get("/orders")
def get_orders(service: OrderService = Depends(OrderService)) -> list[schemas.Order]:
    orders = service.get_orders()
    return orders


@order_router.get("/orders/{order_id}")
def get_order(order_id: int, service: OrderService = Depends(OrderService)) -> schemas.Order:
    order = service.get_order(order_id)
    return order


@order_router.put("/orders/{order_id}")
def update_order(
    order_id: int,
    order: schemas.OrderUpdate,
    service: OrderService = Depends(OrderService),
) -> schemas.Order:
    order = service.update_order(order_id, order)
    service.commit()
    return order


@order_router.delete("/orders/{order_id}")
def delete_order(order_id: int, service: OrderService = Depends(OrderService)):
    msg = service.delete_order(order_id)
    service.commit()
    return msg
