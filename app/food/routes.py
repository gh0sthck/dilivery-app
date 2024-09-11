from typing import Annotated, List, Optional

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


@food_router.post("/add/")
async def food_add(
    schema: Annotated[FoodSchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> FoodSchema:
    return await food_explorer.post(session=session, schema=schema)


@food_router.delete("/{id}/")
async def food_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[FoodSchema]:
    return await food_explorer.delete(session=session, id=id)
