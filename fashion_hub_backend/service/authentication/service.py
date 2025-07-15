from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.database.users import models as user_models
from fashion_hub_backend.errors import APIBadRequest, APINotFound
from fashion_hub_backend.schemas.authentication import schemas as auth_schemas
from fashion_hub_backend.schemas.users import schemas as user_schemas
from fashion_hub_backend.utils.hashing import Hash
from fashion_hub_backend.utils.token import create_access_token


class AuthenticationService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def commit(self):
        return self.db.commit()

    def login_user(self, login_data: auth_schemas.LogIn):
        user = self.db.scalars(user_models.Users.select().where(user_models.Users.email == login_data.username)).first()

        if not user:
            raise APINotFound(key=login_data.username, detail=f"User with email: '{login_data.username}' not found")

        if not Hash.verify(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid password for user: '{login_data.username}'",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.disabled:
            raise APIBadRequest(detail="User is disabled. Please activate the user and try again.")
        access_token = create_access_token(data={"sub": user.email})
        return auth_schemas.Token(access_token=access_token, token_type="bearer")

    def sign_up(self, user: user_schemas.UserCreate):
        user_exists = self.db.scalars(
            user_models.Users.select()
            .where(user_models.Users.email == user.email)
            .where(user_models.Users.phone_number == user.phone_number)
        ).first()

        if user_exists:
            raise APIBadRequest(
                detail=f"User with email: {user.email} and phone number: {user.phone_number} already exists"
            )
        user.password = Hash.bcrypt(user.password)
        user = user.model_dump(exclude_unset=True)
        query = user_models.Users.insert().values([user])
        new_user = self.db.scalars(query).first()
        self.commit()
        return user_schemas.User.model_validate(new_user, from_attributes=True)
