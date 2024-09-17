from datetime import timedelta
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.settings import config

class UserSchema(BaseModel):
    username: str = Field(max_length=80)
    full_name: str = Field(max_length=256)
    email: EmailStr
    password: bytes
    city: int 


class RegisterUser(UserSchema):
    password: str


class JWTPayload(BaseModel):
    sub: int
    username: str
    email: EmailStr
    expire: int = (datetime.now() + timedelta(minutes=config.auth.access_token_expire_minutes)).minute


class JWTToken(BaseModel):
    access_token: bytes
    access_type: str = "Bearer"
