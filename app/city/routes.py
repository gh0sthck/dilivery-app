from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends

from app.city.models import City
from app.city.schema import CitySchema
from app.db_explorer import DbExplorer


city_router = APIRouter(prefix="/api/city", tags=["City"])
city_explorer = DbExplorer(model=City, schema=CitySchema)


@city_router.get("/all/")
async def city_all() -> Optional[List[CitySchema]]:
    return await city_explorer.get()


@city_router.get("/{id}/")
async def city_by_id(id: int) -> Optional[CitySchema]:
    return await city_explorer.get(id=id)


@city_router.post("/add/")
async def city_add(
    schema: Annotated[CitySchema, Depends()],
) -> CitySchema:
    return await city_explorer.post(schema=schema)


@city_router.put("/update/{id}/")
async def city_update(
    id: int,
    schema: Annotated[CitySchema, Depends()],
) -> Optional[CitySchema]:
    return await city_explorer.update(id=id, schema=schema)


@city_router.delete("/delete/{id}")
async def city_delete(id: int) -> Optional[CitySchema]:
    return await city_explorer.delete(id=id)
