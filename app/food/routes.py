from typing import List, Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends

from app.database import get_async_session
from app.db_explorer import DbExplorer
from app.food.models import Food
from app.food.schemas import FoodSchema

food_router = APIRouter(prefix="/food", tags=["Food"])
food_explorer = DbExplorer(model=Food, schema=FoodSchema)


@food_router.get("/all/")
async def food_all(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[List[FoodSchema]]:
    return await food_explorer.get(session=session)


@food_router.get("/{id}/")
async def food_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[FoodSchema]:
    return await food_explorer.get(session=session, id=id)

