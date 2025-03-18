"""
DbExplorer suppose you write less code at CRUD operations writing. Instead writing new CRUD
requests in each route function, you can use already implemented methods in DbExplorer.
You should have model (app.database) and model schema (pydantic.BaseModel) objects to use explorer.
"""

from functools import wraps
from logging import Logger
from typing import Callable, List, Optional

from pydantic import BaseModel
from sqlalchemy import Delete, Insert, Select, Update
from sqlalchemy.ext.asyncio.session import AsyncSession

from .database import async_session
from app.database import Model
from .log import AppLogger


class DbExplorer:
    """
    Easy Database CRUD with SQLAlchemy.

    :self.model: SQLAlchemy model - requires to model have `id` field. Inheritance all models from
    `Model` (app.database).
    :self.schema: Pydantic schema
    :self.session: SQLAlchemy AsyncSession, not required
    """

    LOGGER = AppLogger(__name__)

    def __init__(
        self, model: Model, schema: BaseModel
    ) -> None:
        self.model: Model = model
        self.schema: BaseModel = schema
        self.logger: Logger = self.LOGGER.get_logger()

    def _log(func: Callable):
        wraps(func)

        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except Exception as exc:
                self.logger.error(exc)

        return wrapper

    @_log
    async def get(
        self, id: Optional[int] = None, _session: AsyncSession = async_session()
    ) -> Optional[List[BaseModel] | BaseModel]:
        """
        Return all objects schemas from database; one if id is specified; None if object not found.
        """
        # session: AsyncSession
        async with _session as session:
            query = (
                Select(self.model).where(self.model.id == id)
                if id is not None
                else Select(self.model)
            )
            pre_result = await session.execute(query)
            if id is not None:
                result = pre_result.scalar_one_or_none()
                self.logger.info(f"Result = {result}")
                if result:
                    return self.schema.model_validate(obj=result, from_attributes=True)
                return None

            self.logger.info(f"Multiple result")
            return (
                [
                    self.schema.model_validate(res, from_attributes=True)
                    for res in pre_result.scalars().all()
                ]
                if pre_result
                else None
            )

    @_log
    async def post(
        self, schema: BaseModel, _session: AsyncSession = async_session()
    ) -> BaseModel:
        """Return object schema, which be added to database."""
        async with _session as session:
            query = Insert(self.model).values(schema.model_dump())
            q = await session.execute(query)
            pk = q.inserted_primary_key[0]
            s = schema.model_dump()
            s["id"] = pk
            self.logger.debug(f"Dict schema = {s}")
            await session.commit()
        return self.schema.model_validate(s)

    @_log
    async def delete(
        self, id: int, _session: AsyncSession = async_session()
    ) -> Optional[BaseModel]:
        """Return object schema, which be delete from database."""
        async with _session as session:
            obj: Optional[Model] = await self.get(id=id, _session=session)
            if obj:
                query = Delete(self.model).where(self.model.id == id)
                await session.execute(query)
                s = self.schema.model_validate(obj, from_attributes=True)
                s.id = id
                self.logger.debug(f"Dict schema = {s}")
                await session.commit()
                return self.schema.model_validate(s)
            return None

    @_log
    async def update(
        self, id: int, schema: BaseModel, _session: AsyncSession = async_session()
    ) -> Optional[BaseModel]:
        """Return updated object schema, with be edited in database."""
        async with _session as session:
            obj: Optional[Model] = await self.get(id=id, _session=session)
            if obj:
                query = (
                    Update(self.model)
                    .where(self.model.id == id)
                    .values(schema.model_dump())
                )
                await session.execute(query)
                await session.commit()
                s = schema.model_dump()
                s["id"] = id
                self.logger.debug(f"Dict schema = {s}")
                return self.schema.model_validate(s)
        return None
