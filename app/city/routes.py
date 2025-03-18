from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.city.models import City
from app.city.schema import CitySchema, CitySchemaRead
from app.database import get_async_session
from app.db_explorer import DbExplorer
from app.log import AppLogger


city_router = APIRouter(prefix="/api/city", tags=["City"])
city_explorer = DbExplorer(model=City, schema=CitySchemaRead)

LOGGER = AppLogger("city")
city_logger = LOGGER.get_logger()


@city_router.get("/all/")
async def city_all(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[List[CitySchemaRead]]:
    city_logger.info("City all endpoint")
    return await city_explorer.get(_session=session)


@city_router.get("/{id}/")
async def city_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CitySchemaRead]:
    city_logger.info("City by id endpoint")
    return await city_explorer.get(id=id, _session=session)


@city_router.post("/add/")
async def city_add(
    schema: CitySchema, session: AsyncSession = Depends(get_async_session)
) -> CitySchema:
    city_logger.info("City add endpoint")
    return await city_explorer.post(schema=schema, _session=session)


@city_router.put("/update/{id}/")
async def city_update(
    id: int, schema: CitySchema, session: AsyncSession = Depends(get_async_session)
) -> Optional[CitySchemaRead]:
    city_logger.info("City update endpoint")
    return await city_explorer.update(id=id, schema=schema, _session=session)


@city_router.delete("/delete/{id}")
async def city_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CitySchemaRead]:
    city_logger.info("City delete endpoint")
    return await city_explorer.delete(id=id, _session=session)
