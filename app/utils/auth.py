from datetime import datetime, timedelta, timezone

from jose import jwt
from app.config import settings


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

#     class Config:
#         env_file = ".env"


# settings = Settings()


# def create_access_token(data: dict):

#     to_encode = data.copy()

#     expire = datetime.now(timezone.utc) + timedelta(
#         minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#     )

#     to_encode.update({
#         "exp": expire
#     })

#     encoded_jwt = jwt.encode(
#         to_encode,
#         settings.SECRET_KEY,
#         algorithm=settings.ALGORITHM
#     )

#     return encoded_jwt