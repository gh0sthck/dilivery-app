from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import get_async_session
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


LOGGER = AppLogger("food")
food_logger = LOGGER.get_logger()
shop_logger = LOGGER.get_logger()
category_logger = LOGGER.get_logger()


@food_router.get("/all/")
async def food_all(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[List[FoodSchemaRead]]:
    food_logger.info("Food All endpoint")
    return await food_explorer.get(_session=session)


@food_router.get("/{id}/")
async def food_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[FoodSchemaRead]:
    food_logger.info("Food By id endpoint")
    return await food_explorer.get(id=id, _session=session)


@food_router.post("/add/")
async def food_add(
    schema: FoodSchema, session: AsyncSession = Depends(get_async_session)
) -> FoodSchemaRead:
    food_logger.info("Food Add endpoint")
    return await food_explorer.post(schema=schema, _session=session)


@food_router.delete("/delete/{id}/")
async def food_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[FoodSchemaRead]:
    food_logger.info("Food Delete endpoint")
    return await food_explorer.delete(id=id, _session=session)


@food_router.put("/update/{id}/")
async def food_update(
    id: int, schema: FoodSchema, session: AsyncSession = Depends(get_async_session)
) -> Optional[FoodSchemaRead]:
    food_logger.info("Food Update endpoint")
    return await food_explorer.update(id=id, schema=schema, _session=session)


@shop_router.get("/all/")
async def shop_all(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[List[ShopSchemaRead]]:
    shop_logger.info("Shop all endpoint")
    return await shop_explorer.get(_session=session)


@shop_router.get("/{id}/")
async def shop_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[ShopSchemaRead]:
    shop_logger.info("Shop by id endpoint")
    return await shop_explorer.get(id=id, _session=session)


@shop_router.post("/add/")
async def shop_add(
    schema: ShopSchema, session: AsyncSession = Depends(get_async_session)
) -> ShopSchemaRead:
    shop_logger.info("Shop add endpoint")
    return await shop_explorer.post(schema=schema, _session=session)


@shop_router.delete("/delete/{id}")
async def shop_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[ShopSchemaRead]:
    shop_logger.info("Shop delete endpoint")
    return await shop_explorer.delete(id=id, _session=session)


@shop_router.put("/update/{id}")
async def shop_update(
    id: int, schema: ShopSchema, session: AsyncSession = Depends(get_async_session)
) -> Optional[ShopSchemaRead]:
    shop_logger.info("Shop update endpoint")
    return await shop_explorer.update(id=id, schema=schema, _session=session)


@category_router.get("/all/")
async def category_all(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[List[CategorySchemaRead]]:
    category_logger.info("Category all endpoint")
    return await category_explorer.get(_session=session)


@category_router.get("/{id}/")
async def category_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchemaRead]:
    category_logger.info("Category by id endpoint")
    return await category_explorer.get(id=id, _session=session)


@category_router.post("/add/")
async def category_add(
    schema: CategorySchema, session: AsyncSession = Depends(get_async_session)
) -> CategorySchemaRead:
    category_logger.info("Category add endpoint")
    return await category_explorer.post(schema=schema, _session=session)


@category_router.delete("/delete/")
async def category_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchemaRead]:
    category_logger.info("Categroy delete endpoint")
    return await category_explorer.delete(id=id, _session=session)


@category_router.put("/update/{id}")
async def category_update(
    id: int, schema: CategorySchema, session: AsyncSession = Depends(get_async_session)
) -> Optional[CategorySchemaRead]:
    category_logger.info("Category update endpoint")
    return await category_explorer.update(id=id, schema=schema, _session=session)
