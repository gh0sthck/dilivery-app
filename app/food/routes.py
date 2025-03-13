from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from app.db_explorer import DbExplorer
from app.food.models import Category, Food, Shop
from app.food.schemas import (
    CategorySchema,
    CategorySchemaRead,
    FoodSchema,
    FoodSchemaRead,
    ShopSchema,
    ShopSchemaRead,
)
from app.log import AppLogger

food_router = APIRouter(prefix="/api/food", tags=["Food"])
shop_router = APIRouter(prefix="/api/shop", tags=["Shop"])
category_router = APIRouter(prefix="/api/category", tags=["Category"])

food_explorer = DbExplorer(model=Food, schema=FoodSchemaRead)
shop_explorer = DbExplorer(model=Shop, schema=ShopSchemaRead)
category_explorer = DbExplorer(model=Category, schema=CategorySchemaRead)

LOGGER = AppLogger("name")
food_logger = LOGGER.get_logger()


@food_router.get("/all/")
async def food_all() -> Optional[List[FoodSchemaRead]]:
    food_logger.info("Food All endpoint")
    return await food_explorer.get()


@food_router.get("/{id}/")
async def food_by_id(id: int) -> Optional[FoodSchema]:
    food_logger.info("Food By id endpoint")
    return await food_explorer.get(id=id)


@food_router.post("/add/")
async def food_add(
    schema: FoodSchema,
) -> FoodSchemaRead:
    food_logger.info("Food Add endpoint")
    return await food_explorer.post(schema=schema)


@food_router.delete("/delete/{id}/")
async def food_delete(id: int) -> Optional[FoodSchema]:
    food_logger.info("Food Delete endpoint")
    return await food_explorer.delete(id=id)


@food_router.put("/update/{id}")
async def food_update(
    id: int,
    schema: FoodSchema,
) -> Optional[FoodSchema]:
    food_logger.info("Food Update endpoint")
    return await food_explorer.update(id=id, schema=schema)


@shop_router.get("/all/")
async def shop_all() -> Optional[List[ShopSchemaRead]]:
    return await shop_explorer.get()


@shop_router.get("/{id}/")
async def shop_by_id(id: int) -> Optional[ShopSchemaRead]:
    return await shop_explorer.get(id=id)


@shop_router.post("/add/")
async def shop_add(
    schema: ShopSchema,
) -> ShopSchemaRead:
    return await shop_explorer.post(schema=schema)


@shop_router.delete("/delete/{id}")
async def shop_delete(id: int) -> Optional[ShopSchemaRead]:
    return await shop_explorer.delete(id=id)


@shop_router.put("/update/{id}")
async def shop_update(
    id: int,
    schema: ShopSchema,
) -> Optional[ShopSchemaRead]:
    return await shop_explorer.update(id=id, schema=schema)


@category_router.get("/all/")
async def category_all() -> Optional[List[CategorySchemaRead]]:
    return await category_explorer.get()


@category_router.get("/{id}/")
async def category_by_id(id: int) -> Optional[CategorySchemaRead]:
    return await category_explorer.get(id=id)


@category_router.post("/add/")
async def category_add(schema: CategorySchema) -> CategorySchemaRead:
    return await category_explorer.post(schema=schema)


@category_router.delete("/delete/")
async def category_delete(id: int) -> Optional[CategorySchemaRead]:
    return await category_explorer.delete(id=id)


@category_router.put("/update/{id}")
async def category_update(
    id: int, schema: CategorySchema
) -> Optional[CategorySchemaRead]:
    return await category_explorer.update(id=id, schema=schema)
