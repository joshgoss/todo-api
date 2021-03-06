from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = (datetime.utcnow() + expires_delta).timestamp()
    else:
        expire = (
            datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        ).timestamp()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.access_token_algorithm
    )

    return {"access_token": encoded_jwt, "expiration": expire, "token_type": "bearer"}
