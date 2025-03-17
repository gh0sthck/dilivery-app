from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends

from app.city.models import City
from app.city.schema import CitySchema, CitySchemaRead
from app.db_explorer import DbExplorer
from app.log import AppLogger


city_router = APIRouter(prefix="/api/city", tags=["City"])
city_explorer = DbExplorer(model=City, schema=CitySchemaRead)

LOGGER = AppLogger("city")
city_logger = LOGGER.get_logger()


@city_router.get("/all/")
async def city_all() -> Optional[List[CitySchemaRead]]:
    city_logger.info("City all endpoint") 
    return await city_explorer.get()


@city_router.get("/{id}/")
async def city_by_id(id: int) -> Optional[CitySchemaRead]:
    city_logger.info("City by id endpoint") 
    return await city_explorer.get(id=id)


@city_router.post("/add/")
async def city_add(
    schema: CitySchema,
) -> CitySchema:
    city_logger.info("City add endpoint")
    return await city_explorer.post(schema=schema)


@city_router.put("/update/{id}/")
async def city_update(
    id: int,
    schema: CitySchema,
) -> Optional[CitySchemaRead]:
    city_logger.info("City update endpoint")
    return await city_explorer.update(id=id, schema=schema)


@city_router.delete("/delete/{id}")
async def city_delete(id: int) -> Optional[CitySchemaRead]:
    city_logger.info("City delete endpoint") 
    return await city_explorer.delete(id=id)
