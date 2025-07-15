from fastapi import APIRouter, Depends

from fashion_hub_backend.schemas.authentication import schemas as auth_schema
from fashion_hub_backend.schemas.users import schemas as user_schema
from fashion_hub_backend.service.authentication.service import AuthenticationService

authentication_router = APIRouter(prefix="", tags=["authentication"])


@authentication_router.post("/login")
def login(login_data: auth_schema.LogIn = Depends(), service: AuthenticationService = Depends()):
    # login_data = auth_schema.LogIn(
    #     username=login_data.username,
    #     password=login_data.password
    # )
    token = service.login_user(login_data)
    return token


@authentication_router.post("/signup", response_model=user_schema.User)
def signup(user_data: user_schema.UserCreate, service: AuthenticationService = Depends()):
    new_user = service.sign_up(user_data)
    return new_user
