
from fashion_hub_backend.utils.base_schemas import BaseSchema

class LogIn(BaseSchema):
    username: str
    password: str

class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    email: str | None = None

class User(BaseSchema):
    username: str