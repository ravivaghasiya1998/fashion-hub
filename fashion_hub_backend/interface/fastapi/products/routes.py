import os
from fastapi import APIRouter, Depends, status, UploadFile, File, Body, Query, Form

from fashion_hub_backend.schemas.products import schemas
from fashion_hub_backend.schemas.authentication import schemas as auth_schema
from fashion_hub_backend.service.products.service import ProductService
from fashion_hub_backend.errors import APIBadRequest
from datetime import datetime
from fashion_hub_backend.utils.oauth2 import get_current_active_user


product_router = APIRouter(prefix="/v1", tags=["products"],dependencies=[Depends(get_current_active_user)])

# Create an upload directory if it doesn't exist
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "images")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def parse_product_query(
    title: str = Query(...),
    description: str = Query(...),
    price: float = Query(...),
    stock_quantity: int = Query(...),
    category_id: int = Query(...),
    category_name: str = Query(...),
) -> schemas.ProductCreate:
    return schemas.ProductCreate(
        title=title,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        category_id=category_id,
        category_name=category_name,
    )

@product_router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(
    
    image: UploadFile ,
    product: schemas.ProductCreate = Depends(parse_product_query), 
    service: ProductService = Depends()

) -> schemas.Product:
    
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    file_extension = image.filename.split(".")[-1]
    if file_extension.lower() not in ALLOWED_EXTENSIONS:
        raise APIBadRequest(
            detail=f"Unsupported file type: {file_extension}. Only {ALLOWED_EXTENSIONS} are allowed.",
        )

    # Step 2: Save the uploaded image to the 'images' folder
    image_filename = f"{product.title}_{image.filename}"
    image_path = os.path.join(UPLOAD_DIRECTORY, image_filename)
    
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())  # Save binary data
    rel_path = os.path.relpath(image_path, os.getcwd())
    product = schemas.ProductCreateWithImage(**product.model_dump(), image_path=rel_path)
    product = service.create_product(product)
    return product


@product_router.get("/products")
def get_products(service: ProductService = Depends()) -> list[schemas.Product]:
    products = service.get_products()
    return products


@product_router.get("/products/{product_id}")
def get_product(
    product_id: int, service: ProductService = Depends()
) -> schemas.Product:
    product = service.get_product(product_id)
    return product


@product_router.put("/products/{product_id}")
def update_product(
    product_id: int, product: schemas.ProductCreate, service: ProductService = Depends()
) -> schemas.Product:
    product = service.update_product(product_id, product)
    service.commit()
    return product


@product_router.delete("/products/{product_id}")
def delete_product(product_id: int, service: ProductService = Depends()):
    msg = service.delete_product(product_id)
    service.commit()
    return msg
