from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response

from app.auth.schemas import JWTPayload, JWTToken, RegisterUser, UserSchema
from app.auth.user_explorer import UserExplorer
from app.auth.utils import decode_jwt, hash_password, validate_password, encode_jwt


users_router = APIRouter(prefix="/api/auth", tags=["Auth"])
users_explorer = UserExplorer()


async def validate_auth_user(username: str = Form(), password: str = Form()):
    user = await users_explorer.get_by_username(username=username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if validate_password(password=password, hash=user.password):
        return user
    raise HTTPException(status_code=401, detail="Invalid username or password")


async def get_token(request: Request) -> dict:
    token = request.cookies.get("access_token")
    print("TOKEN", token)
    if token:
        return decode_jwt(jwt_token=token)
    raise HTTPException(status_code=401, detail="Unauthenticated.")


async def get_current_user(
    token: dict = Depends(get_token)
):
    user = await users_explorer.get_by_username(username=token.get("username"))
    return user


@users_router.post("/login/")
async def user_login(response: Response, schema: UserSchema = Depends(validate_auth_user)) -> JWTToken:
    schema.password = hash_password(schema.password.decode()).decode()
    payload = JWTPayload(
        sub=schema.username, username=schema.username, email=schema.email
    )
    token = encode_jwt(payload=payload)
    response.set_cookie(
        key="access_token",
        value=token.decode(),
        httponly=True
    )
    return JWTToken(access_token=token)


@users_router.post("/logout/")
async def users_logout(request: Request, response: Response) -> dict:
    if request.cookies.get("access_token"):
        response.delete_cookie("access_token") 
        return {"status": 200}
    raise HTTPException(status_code=401, detail="Unauthenticated.")


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


@users_router.get("/all/")
async def user_all() -> Optional[List[UserSchema]]:
    return await users_explorer.get()


@users_router.get("/{id}/")
async def user_by_id(id: int) -> UserSchema:
    return await users_explorer.get(id=id)
