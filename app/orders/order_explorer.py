from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.schemas import SOrder
from app.orders.models import Order
from app.db_explorer import DbExplorer
from app.database import async_session


class OrderExplorer(DbExplorer):
    def __init__(self):
        super().__init__(Order, SOrder)

    async def get(
        self, id: Optional[int] = None
    ) -> Optional[List[BaseModel] | BaseModel]:
        session: AsyncSession
        async with async_session() as session:
            query = (
                Select(self.model).where(self.model.columns[0] == id)
                if id
                else Select(self.model)
            )
            pre_result = await session.execute(query)
            if id is not None:
                result = pre_result.fetchone()
                if result:
                    return self.schema(
                        user_id=result[1], courier_id=result[2], status=result[3]
                    )
                return None
            return (
                [
                    self.schema(user_id=res[1], courier_id=res[2], status=res[3])
                    for res in pre_result.all()
                ]
                if pre_result
                else None
            )
