from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Select
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
        """Return all objects from database; one if id is specified; None if object not found."""
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

    async def post(self, session: AsyncSession, schema: BaseModel) -> BaseModel: ...

    async def delete(self, session: AsyncSession) -> BaseModel: ...

    async def update(
        self, session: AsyncSession, id: int, new_schema: BaseModel
    ) -> BaseModel: ...
