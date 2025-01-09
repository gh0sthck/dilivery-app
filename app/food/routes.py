from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from app.db_explorer import DbExplorer
from app.food.models import Category, Food, Shop
from app.food.schemas import CategorySchema, FoodSchema, ShopSchema

food_router = APIRouter(prefix="/api/food", tags=["Food"])
shop_router = APIRouter(prefix="/api/shop", tags=["Shop"])
category_router = APIRouter(prefix="/api/category", tags=["Category"])

food_explorer = DbExplorer(model=Food, schema=FoodSchema)
shop_explorer = DbExplorer(model=Shop, schema=ShopSchema)
category_explorer = DbExplorer(model=Category, schema=CategorySchema)


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


@shop_router.post("/add/")
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


@category_router.get("/all/")
async def category_all() -> Optional[List[CategorySchema]]:
    return await category_explorer.get()


@category_router.get("/{id}/")
async def caetgory_by_id(id: int) -> Optional[CategorySchema]:
    return await category_explorer.get(id=id)


@category_router.post("/add/")
async def category_add(schema: Annotated[CategorySchema, Depends()]) -> CategorySchema:
    return await category_explorer.post(schema=schema)


@category_router.delete("/delete/")
async def category_delete(id: int) -> Optional[CategorySchema]:
    return await category_explorer.delete(id=id)


@category_router.put("/update/{id}")
async def category_update(id: int, schema: CategorySchema) -> Optional[CategorySchema]:
    return await category_explorer.update(id=id, schema=schema)
