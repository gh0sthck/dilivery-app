from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.city.models import City
from app.city.schema import CitySchema
from app.database import get_async_session
from app.db_explorer import DbExplorer


city_router = APIRouter(prefix="/city", tags=["City"])
city_explorer = DbExplorer(model=City, schema=CitySchema)


@city_router.get("/all/")
async def city_all(
    session: AsyncSession = Depends(get_async_session),
) -> Optional[List[CitySchema]]:
    return await city_explorer.get(session=session)


@city_router.get("/{id}/")
async def city_by_id(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CitySchema]:
    return await city_explorer.get(id=id, session=session)


@city_router.post("/new/")
async def city_add(
    schema: Annotated[CitySchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> CitySchema:
    return await city_explorer.post(session=session, schema=schema)


@city_router.put("/update/{id}/")
async def city_update(
    id: int,
    schema: Annotated[CitySchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> Optional[CitySchema]:
    return await city_explorer.update(session=session, id=id, schema=schema)


@city_router.delete("/delete/{id}")
async def city_delete(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> Optional[CitySchema]:
    return await city_explorer.delete(session=session, id=id)
