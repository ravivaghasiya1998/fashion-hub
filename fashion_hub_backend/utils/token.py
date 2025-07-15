from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from fashion_hub_backend.schemas.authentication import schemas as auth_schemas

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JWTSetting(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

jwtconfig = JWTSetting()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwtconfig.secret_key, algorithm=jwtconfig.algorithm)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, jwtconfig.secret_key, algorithms=[jwtconfig.algorithm])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception #noqa: B904

    return token_data
