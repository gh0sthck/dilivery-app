from datetime import timedelta
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.settings import config


class SUserView(BaseModel):
    id: int
    username: str = Field(max_length=80)
    full_name: str = Field(max_length=256)
    email: EmailStr
    balance: float = 0.0
    city: int
    role: int


class SUser(SUserView):
    password: str
    order_create: Optional[bool] = False


class SRegisterUser(BaseModel):
    username: str = Field(max_length=80)
    full_name: str = Field(max_length=256)
    email: EmailStr
    city: int
    password: str


class JWTPayload(BaseModel):
    sub: str
    username: str
    email: EmailStr
    expire: int = (
        datetime.now() + timedelta(minutes=config.auth.access_token_expire_minutes)
    ).minute


class JWTToken(BaseModel):
    access_token: bytes
    access_type: str = "Bearer"
