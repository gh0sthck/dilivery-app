from typing import Annotated, List, Optional

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends

from app.database import get_async_session
from app.db_explorer import DbExplorer
from app.food.models import Food, Shop
from app.food.schemas import FoodSchema, ShopSchema

food_router = APIRouter(prefix="/food", tags=["Food"])
shop_router = APIRouter(prefix="/shop", tags=["Shop"])

food_explorer = DbExplorer(model=Food, schema=FoodSchema)
shop_explorer = DbExplorer(model=Shop, schema=ShopSchema)


@food_router.get("/all/")
async def food_all() -> Optional[List[FoodSchema]]:
    return await food_explorer.get()


@food_router.get("/{id}/")
async def food_by_id(id: int) -> Optional[FoodSchema]:
    return await food_explorer.get(id=id)


@food_router.post("/add/")
async def food_add(
    schema: Annotated[FoodSchema, Depends()],
) -> FoodSchema:
    return await food_explorer.post(schema=schema)


@food_router.delete("/delete/{id}/")
async def food_delete(id: int) -> Optional[FoodSchema]:
    return await food_explorer.delete(id=id)


@food_router.put("/update/{id}")
async def food_update(
    id: int,
    schema: Annotated[FoodSchema, Depends()],
) -> Optional[FoodSchema]:
    return await food_explorer.update(id=id, schema=schema)


@shop_router.get("/all/")
async def shop_all() -> Optional[List[ShopSchema]]:
    return await shop_explorer.get()


@shop_router.get("/{id}/")
async def shop_by_id(id: int) -> Optional[ShopSchema]:
    return await shop_explorer.get(id=id)


@shop_router.post("/new/")
async def shop_add(
    schema: Annotated[ShopSchema, Depends()],
) -> ShopSchema:
    return await shop_explorer.post(schema=schema)


@shop_router.delete("/delete/{id}")
async def shop_delete(id: int) -> Optional[ShopSchema]:
    return await shop_explorer.delete(id=id)


@shop_router.put("/update/{id}")
async def shop_update(
    id: int,
    schema: Annotated[ShopSchema, Depends()],
) -> Optional[ShopSchema]:
    return await shop_explorer.update(id=id, schema=schema)
