from fastapi import Depends
from sqlalchemy.orm import Session

from fashion_hub_backend.database.categories import models as category_models
from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.database.products import models
from fashion_hub_backend.errors import APIBadRequest, APINotFound
from fashion_hub_backend.schemas.products import schemas


class ProductService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def create_product(self, product: schemas.ProductCreateWithImage):
        category_exists = self.db.scalars(
            category_models.Categories.select().where(
                category_models.Categories.id == product.category_id
            )
        ).first()
        if not category_exists:
            raise APIBadRequest(
                detail=f"Category with id: {product.category_id} does not exist"
            )
        product_exists = self.db.scalars(
            models.Products.select().where(models.Products.title == product.title)
        ).first()
        if product_exists:
            raise APIBadRequest(
                detail=f"Product with name: {product.title} already exists"
            )
        new_product = models.Products(**product.model_dump())
        self.db.add(new_product)
        self.commit()
        # product = product.model_dump(exclude_unset=True)
        # query = models.Products.insert().values([product])
        # new_product = self.db.scalars(query).first()
        return schemas.Product.model_validate(new_product, from_attributes=True)

    def get_product(self, product_id: int):
        product = self.db.scalars(
            models.Products.select().where(models.Products.id == product_id)
        ).first()
        if not product:
            raise APINotFound(detail=f"Product with id: {product_id} does not exist")
        return schemas.Product.model_validate(product, from_attributes=True)

    def get_products(self):
        products = self.db.scalars(models.Products.select()).all()
        if products is None:
            raise APINotFound(detail="No products found")
        return [
            schemas.Product.model_validate(product, from_attributes=True)
            for product in products
        ]

    def update_product(self, product_id: int, product: schemas.ProductCreate):
        product_exists = self.db.scalars(
            models.Products.select().where(models.Products.id == product_id)
        ).first()
        if not product_exists:
            raise APINotFound(detail=f"Product with id: {product_id} does not exist")
        if product.title is not None:
            product_exists.title = product.title
        if product.description is not None:
            product_exists.description = product.description
        if product.price is not None:
            product_exists.price = product.price
        if product.stock_quantity is not None:
            product_exists.stock_quantity = product.stock_quantity

        return schemas.Product.model_validate(product_exists, from_attributes=True)

    def delete_product(self, product_id: int):
        product = self.db.scalars(
            models.Products.select().where(models.Products.id == product_id)
        ).first()
        if product is None:
            raise APINotFound(detail=f"Product with id: {product_id} does not exist")
        self.db.delete(product)
        msg = f"Product with id: {product_id} has been deleted"
        return msg
