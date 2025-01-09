from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response

from app.auth.schemas import JWTPayload, JWTToken, SUser, SUserView, SRegisterUser
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
    if token:
        return decode_jwt(jwt_token=token)
    raise HTTPException(status_code=401, detail="Unauthenticated.")


async def get_current_user(token: dict = Depends(get_token)) -> Optional[SUser]:
    user = await users_explorer.get_by_username(username=token.get("username"))
    return user


@users_router.post("/login/")
async def user_login(
    response: Response, schema: SUser = Depends(validate_auth_user)
) -> JWTToken:
    schema.password = hash_password(schema.password).decode()
    payload = JWTPayload(
        sub=schema.username, username=schema.username, email=schema.email
    )
    token = encode_jwt(payload=payload)
    response.set_cookie(key="access_token", value=token.decode(), httponly=True)
    return JWTToken(access_token=token)


@users_router.post("/logout/")
async def users_logout(request: Request, response: Response) -> dict:
    if request.cookies.get("access_token"):
        response.delete_cookie("access_token")
        return {"status": 200}
    raise HTTPException(status_code=401, detail="Unauthenticated.")


@users_router.post("/register/")
async def user_register(schema: SRegisterUser = Depends()) -> SUser:
    temp = schema.model_dump()
    temp["role"] = 0
    temp["password"] = hash_password(temp["password"]).decode() 
    schema = SUser.model_validate(temp)
    return await users_explorer.post(schema=schema)


@users_router.post("/me/")
async def user_current_user(
    schema: SUserView = Depends(get_current_user),
) -> SUserView:
    return schema


def compare(cu: SUserView, u: SUserView) -> SUserView:
    if cu.username == u.username: 
        return u
    else:
        u.balance = None
        return u 


@users_router.get("/all/")
async def user_all(current_user: SUser = Depends(get_current_user)) -> Optional[List[SUserView]]:
    users: Optional[list[SUser]] = await users_explorer.get()
    if users:
        return [compare(current_user, SUserView.model_validate(us)) for us in users]


@users_router.get("/{id}/")
async def user_by_id(id: int, current_user: SUser = Depends(get_current_user)) -> Optional[SUserView]:
    user: Optional[SUser] = await users_explorer.get(id=id)
    if user:
        return compare(current_user, SUserView.model_validate(user))
