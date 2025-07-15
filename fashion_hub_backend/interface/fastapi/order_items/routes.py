from fastapi import APIRouter, Depends, status

from fashion_hub_backend.schemas.order_items import schemas
from fashion_hub_backend.service.order_items.service import OrderItemService
from fashion_hub_backend.utils.oauth2 import get_current_active_user

order_item_router = APIRouter(prefix="/v1", tags=["order_items"], dependencies=[Depends(get_current_active_user)])


@order_item_router.post("/order_items", status_code=status.HTTP_201_CREATED)
def create_order(
    order_item: schemas.OrderedItemCreate,
    service: OrderItemService = Depends(OrderItemService),
) -> schemas.OrderedItem:
    order_item = service.create_order_item(order_item)
    service.commit()
    return order_item


@order_item_router.get("/order_items")
def get_orders(
    service: OrderItemService = Depends(OrderItemService),
) -> list[schemas.OrderedItem]:
    orders = service.get_order_items()
    return orders


@order_item_router.get("/order_items/{order_item_id}")
def get_order(order_item_id: int, service: OrderItemService = Depends(OrderItemService)) -> schemas.OrderedItem:
    order = service.get_order_item(order_item_id)
    return order


@order_item_router.put("/order_items/{order_item_id}")
def update_order(
    order_item_id: int,
    order_item: schemas.OrderedItemUpdate,
    service: OrderItemService = Depends(OrderItemService),
) -> schemas.OrderedItem:
    order_item = service.update_order_item(order_item_id, order_item)
    service.commit()
    return order_item


@order_item_router.delete("/order_items/{order_item_id}")
def delete_order(order_item_id: int, service: OrderItemService = Depends(OrderItemService)):
    msg = service.delete_order_item(order_item_id)
    service.commit()
    return msg
