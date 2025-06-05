from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from fashion_hub_backend.utils.token import verify_token
from fashion_hub_backend.database.users import models as user_models
from fashion_hub_backend.schemas.users import schemas as user_schemas
from fashion_hub_backend.database.db_setup import get_db
from sqlalchemy.orm import Session
from jose import JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
security = HTTPBearer()

# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token_data = verify_token(token, credentials_exception)
#


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = verify_token(token, credentials_exception)
        user = db.scalars(
        user_models.Users.select().where(user_models.Users.email == token_data.email)
        ).first()
        if user is None:
            raise credentials_exception
        return user_schemas.User.model_validate(user, from_attributes=True)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


def get_current_active_user(
    current_user: user_schemas.User = Depends(get_current_user),
):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
