from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fashion_hub_backend.schemas.authentication import schemas as auth_schema
from fashion_hub_backend.service.authentication.service import AuthenticationService
from fashion_hub_backend.schemas.users import schemas as user_schema





authentication_router = APIRouter(prefix="", tags=["authentication"])

@authentication_router.post("/login")
def login(
    login_data: auth_schema.LogIn = Depends(),
    service: AuthenticationService = Depends()):
    # login_data = auth_schema.LogIn(
    #     username=login_data.username,
    #     password=login_data.password
    # )
    token = service.login_user(login_data)
    return token


