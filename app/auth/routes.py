from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.auth.models import User
from app.auth.schemas import RegisterUser, UserSchema
from app.auth.utils import hash_password
from app.database import get_async_session
from app.db_explorer import DbExplorer


users_router = APIRouter(prefix="/auth", tags=["Auth"])
users_explorer = DbExplorer(model=User, schema=UserSchema)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form()
):
    unauth_exception = HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )
    
    async with get_async_session() as sess: 
        user = users_explorer.get(session=sess) 
    
    if not user:
        raise unauth_exception


@users_router.post("/login/")
async def user_login(schema: Annotated[RegisterUser, Depends()], session: AsyncSession = Depends(get_async_session)):
    schema.password = hash_password(schema.password).decode() 
     
    return {
        "200": "success"
    }
