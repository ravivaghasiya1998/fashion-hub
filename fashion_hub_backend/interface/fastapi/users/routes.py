
from fastapi import APIRouter, Depends, status
from typing import Annotated
from fashion_hub_backend.schemas.users import schemas
from fashion_hub_backend.service.users.service import UserService
from fashion_hub_backend.service.authentication.service import AuthenticationService
from fashion_hub_backend.database.db_setup import get_db
from fashion_hub_backend.utils.oauth2 import get_current_active_user


user_router = APIRouter(prefix="/v1", tags=["users"], dependencies=[Depends(get_current_active_user)])

@user_router.get("/users/me")
def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@user_router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate, service: UserService = Depends()
) -> schemas.User:
    user = service.create_user(user)
    service.commit()
    return user


@user_router.get("/users")
def get_users(service: UserService = Depends()) -> list[schemas.User]:
    users = service.get_users()
    return users


@user_router.get("/users/{user_id}")
def get_user(user_id: int, service: UserService = Depends()) -> schemas.User:
    user = service.get_user(user_id)
    return user


@user_router.put("/users/{user_id}")
def update_user(
    user_id: int, user: schemas.UserUpdare, service: UserService = Depends()
) -> schemas.User:
    user = service.update_user(user_id, user)
    service.commit()
    return user


@user_router.delete("/users/{user_id}")
def delete_user(user_id: int, service: UserService = Depends()):
    msg = service.delete_user(user_id)
    service.commit()
    return msg
