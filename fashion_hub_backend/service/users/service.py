from fastapi import Depends
from sqlalchemy.orm import Session

from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.database.users import models
from fashion_hub_backend.errors import APIBadRequest, APINotFound
from fashion_hub_backend.schemas.users import schemas
from fashion_hub_backend.utils.hashing import Hash


class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def create_user(self, user: schemas.UserCreate):
        user_exists = self.db.scalars(
            models.Users.select()
            .where(models.Users.email == user.email)
            .where(models.Users.phone_number == user.phone_number)
        ).first()

        if user_exists:
            raise APIBadRequest(
                detail=f"User with email: {user.email} and phone number: {user.phone_number} already exists"
            )
        user.password = Hash.bcrypt(user.password)
        user = user.model_dump(exclude_unset=True)
        query = models.Users.insert().values([user])
        new_user = self.db.scalars(query).first()
        return schemas.User.model_validate(new_user, from_attributes=True)

    def get_user(self, user_id: int):
        user = self.db.scalars(
            models.Users.select().where(models.Users.id == user_id)
        ).first()
        if not user:
            raise APINotFound(detail=f"User with id: {user_id} does not exist")
        return schemas.User.model_validate(user, from_attributes=True)

    def get_users(self):
        users = self.db.scalars(models.Users.select()).all()
        if users is None:
            raise APINotFound(detail="No users found")
        return [
            schemas.User.model_validate(user, from_attributes=True) for user in users
        ]

    def update_user(self, user_id: int, user: schemas.UserCreate):
        user_exists = self.db.scalars(
            models.Users.select().where(models.Users.id == user_id)
        ).first()
        if not user_exists:
            raise APINotFound(detail=f"User with id: {user_id} does not exist")
        if user.user_name is not None:
            user_exists.name = user.user_name
        if user.email is not None:
            user_exists.email = user.email
        if user.phone_number is not None:
            user_exists.phone_numbwer = user.phone_number
        if user.address is not None:
            user_exists.address = user.address
        if user.disabled is not None:
            user_exists.disabled = user.disabled
        return schemas.User.model_validate(user_exists, from_attributes=True)

    def delete_user(self, user_id: int):
        user = self.db.scalars(
            models.Users.select().where(models.Users.id == user_id)
        ).first()
        if user is None:
            raise APINotFound(detail=f"User with id: {user_id} does not exist")
        self.db.delete(user)
        msg = f"User with id: {user_id} has been deleted"
        return msg
