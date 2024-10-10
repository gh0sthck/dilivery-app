"""
DbExplorer suppose you write less code at CRUD operations writing. Instead writing new CRUD
requests in each route function, you can use already implemented methods in DbExplorer. 
You should have model (app.database) and model schema (pydantic.BaseModel) objects to use explorer.
"""

from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Delete, Insert, Select, Update
from sqlalchemy.ext.asyncio.session import AsyncSession

from .database import async_session
from app.database import Model


class DbExplorer:
    """
    Easy Database CRUD with SQLAlchemy.

    :self.model: SQLAlchemy model - requires to model have `id` field. Inheritance all models from
    `Model` (app.database).
    :self.schema: Pydantic schema
    """

    def __init__(self, model: Model, schema: BaseModel) -> None:
        self.model: Model = model
        self.schema: BaseModel = schema

    async def get(
        self, id: Optional[int] = None
    ) -> Optional[List[BaseModel] | BaseModel]:
        """
        Return all objects schemas from database; one if id is specified; None if object not found.
        """
        session: AsyncSession
        async with async_session() as session:
            query = (
                Select(self.model).where(self.model.id == id)
                if id
                else Select(self.model)
            )
            pre_result = await session.execute(query)
            if id is not None:
                result = pre_result.scalar_one_or_none()
                if result:
                    return self.schema.model_validate(obj=result.__dict__)
                return None
            return (
                [
                    self.schema.model_validate(obj=res.__dict__)
                    for res in pre_result.scalars().all()
                ]
                if pre_result
                else None
            )

    async def post(self, schema: BaseModel) -> BaseModel:
        """Return object schema, which be added to database."""
        session: AsyncSession
        async with async_session() as session:
            query = Insert(self.model).values(schema.model_dump())
            await session.execute(query)
            await session.commit()
        return schema

    async def delete(self, id: int) -> Optional[BaseModel]:
        """Return object schema, which be delete from database."""
        session: AsyncSession
        async with async_session() as session:
            obj: Optional[self.model] = await self.get(session=session, id=id)
            if obj:
                query = Delete(self.model).where(self.model.id == id)
                await session.execute(query)
                await session.commit()
                return self.schema.model_validate(obj.__dict__)
            return None

    async def update(self, id: int, schema: BaseModel) -> Optional[BaseModel]:
        """Return updated object schema, with be edited in database."""
        session: AsyncSession
        async with async_session() as session:
            obj: Optional[self.model] = await self.get(session=session, id=id)
            if obj:
                query = (
                    Update(self.model)
                    .where(self.model.id == id)
                    .values(schema.model_dump())
                )
                await session.execute(query)
                await session.commit()
                return schema
        return None
