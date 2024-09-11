"""
DbExplorer suppose you write less code at CRUD operations writing. Instead writing new CRUD
requests in each route function, you can use already implemented methods in DbExplorer. 
You should have model (app.database) and model schema (pydantic.BaseModel) objects to use explorer.
"""

from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Delete, Insert, Select
from sqlalchemy.ext.asyncio.session import AsyncSession

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
        self, session: AsyncSession, id: Optional[int] = None
    ) -> Optional[List[BaseModel] | BaseModel]:
        """
        Return all objects schemas from database; one if id is specified; None if object not found.
        """
        async with session as sess:
            query = (
                Select(self.model).where(self.model.id == id)
                if id
                else Select(self.model)
            )
            pre_result = await session.execute(query)
            if id:
                return pre_result.scalar_one_or_none()
            return pre_result.scalars().all()

    async def post(self, session: AsyncSession, schema: BaseModel) -> BaseModel:
        """Return object schema, which be added to database."""
        async with session as sess:
            query = Insert(self.model).values(schema.model_dump())
            await sess.execute(query)
            await sess.commit()
        return schema

    async def delete(self, session: AsyncSession, id: int) -> Optional[BaseModel]:
        """Return object schema, which be delete from database."""
        food: Optional[self.model] = await self.get(session=session, id=id)
        if food:
            async with session as sess:
                query = Delete(self.model).where(self.model.id == id)
                await sess.execute(query)
                await sess.commit()
            return self.schema.model_validate(food.__dict__)
        return None

    async def update(
        self, session: AsyncSession, id: int, new_schema: BaseModel
    ) -> BaseModel:
        """Return updated object schema, with be edited in database."""
        pass
