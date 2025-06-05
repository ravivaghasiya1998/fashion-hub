from datetime import datetime
from typing import Optional

from fashion_hub_backend.utils.base_schemas import BaseSchema


class UserBase(BaseSchema):
    user_name: str
    email: str
    #password: str
    phone_number: str | None = None
    address: str
    disabled :bool = False
    

class User(UserBase):
    created_at: datetime
    id: int


class UserCreate(UserBase):
    password: str

class ShowUser(BaseSchema):
    user_name: str
    email: str
    phone_number: str | None = None
    address: str

class UserUpdare(BaseSchema):
    user_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    disabled: Optional[bool] = False