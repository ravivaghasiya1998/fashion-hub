from fastapi import Depends
from sqlalchemy.orm import Session

from fashion_hub_backend.database.categories import models
from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.errors import APIBadRequest, APINotFound
from fashion_hub_backend.schemas.categories import schemas


class CategoryService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def create_catogory(self, category: schemas.CategoryCreate):
        category_exists = self.db.scalars(
            models.Categories.select().where(models.Categories.name == category.name)
        ).first()
        if category_exists:
            raise APIBadRequest(
                detail=f"Category with name: {category.name} already exists"
            )

        category = category.model_dump(exclude_unset=True)
        query = models.Categories.insert().values([category])
        new_category = self.db.scalars(query).first()
        return schemas.Category.model_validate(new_category, from_attributes=True)

    def get_category(self, category_id: int):
        category = self.db.scalars(
            models.Categories.select().where(models.Categories.id == category_id)
        ).first()
        if not category:
            raise APINotFound(detail=f"Category with id: {category_id} does not exist")
        return schemas.Category.model_validate(category, from_attributes=True)

    def get_categories(self):
        categories = self.db.scalars(models.Categories.select()).all()
        if categories is None:
            raise APINotFound(detail="No Categories found")
        return [
            schemas.Category.model_validate(category, from_attributes=True)
            for category in categories
        ]

    def update_category(self, category_id: int, category: schemas.CategoryCreate):
        category_exists = self.db.scalars(
            models.Categories.select().where(models.Categories.id == category_id)
        ).first()
        if not category_exists:
            raise APINotFound(detail=f"Category with id: {category_id} does not exist")
        if category.name is not None:
            category_exists.name = category.name
        if category.description is not None:
            category_exists.description = category.description

        return schemas.Category.model_validate(category_exists, from_attributes=True)

    def delete_category(self, category_id: int):
        category = self.db.scalars(
            models.Categories.select().where(models.Categories.id == category_id)
        ).first()
        if category is None:
            raise APINotFound(detail=f"Category with id: {category_id} does not exist")
        self.db.delete(category)
        msg = f"Category with id: {category_id} has been deleted"
        return msg
