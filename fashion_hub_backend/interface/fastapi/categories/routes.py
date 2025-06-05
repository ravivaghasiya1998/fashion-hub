from fastapi import APIRouter, Depends, status

from fashion_hub_backend.schemas.categories import schemas
from fashion_hub_backend.service.categories.service import CategoryService
from fashion_hub_backend.utils.oauth2 import get_current_active_user

category_router = APIRouter(prefix="/v1", tags=["categories"], dependencies=[Depends(get_current_active_user)])


@category_router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(
    name: schemas.CategoryName,
    description: str,
    service: CategoryService = Depends()
) -> schemas.Category:
    category= schemas.CategoryCreate(name=name,description=description)
    category = service.create_catogory(category)
    service.commit()
    return category


@category_router.get("/categories")
def get_categories(service: CategoryService = Depends()) -> list[schemas.Category]:
    categories = service.get_categories()
    return categories


@category_router.get("/categories/{category_id}")
def get_category(
    category_id: int, service: CategoryService = Depends()
) -> schemas.Category:
    category = service.get_category(category_id)
    return category


@category_router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    service: CategoryService = Depends(),
) -> schemas.Category:
    category = service.update_category(category_id, category)
    service.commit()
    return category


@category_router.delete("/categories/{category_id}")
def delete_category(category_id: int, service: CategoryService = Depends()):
    msg = service.delete_category(category_id)
    service.commit()
    return msg
