from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.schemas import JWTPayload, JWTToken, RegisterUser, UserSchema
from app.auth.user_explorer import UserExplorer
from app.auth.utils import decode_jwt, hash_password, validate_password, encode_jwt


users_router = APIRouter(prefix="/api/auth", tags=["Auth"])
users_explorer = UserExplorer()
http_bearer = HTTPBearer()


async def validate_auth_user(username: str = Form(), password: str = Form()):
    unauth_exception = HTTPException(
        status_code=401, detail="Invalid username or password"
    )
    user = await users_explorer.get_by_username(username=username)
    if not user:
        raise unauth_exception
    if validate_password(password=password, hash=user.password):
        return user
    raise unauth_exception


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserSchema:
    token: dict = decode_jwt(jwt_token=creds.credentials.encode())
    current_user = await users_explorer.get_by_username(username=token.get("username"))
    return current_user


@users_router.post("/login/")
async def user_login(schema: UserSchema = Depends(validate_auth_user)) -> JWTToken:
    schema.password = hash_password(schema.password.decode()).decode()
    payload = JWTPayload(
        sub=schema.username, username=schema.username, email=schema.email
    )
    token = encode_jwt(payload=payload)

    return JWTToken(access_token=token)


@users_router.post("/register/")
async def user_register(schema: RegisterUser = Depends()) -> UserSchema:
    schema.password = hash_password(schema.password).decode()
    user = await users_explorer.post(schema=schema)
    return user


@users_router.post("/me/")
async def user_current_user(
    schema: UserSchema = Depends(get_current_user),
) -> UserSchema:
    return schema


@users_router.get("/{id}/")
async def user_by_id(id: int) -> UserSchema:
    return await users_explorer.get(id=id)
