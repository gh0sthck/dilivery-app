from typing import List, Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.schemas import OrderSchema
from .models import Order
from app.db_explorer import DbExplorer
from app.database import async_session


class OrderExplorer(DbExplorer):
    def __init__(self):
        super().__init__(Order, OrderSchema)
    
    async def get(
        self, id: Optional[int] = None
    ) -> Optional[List[OrderSchema] | OrderSchema]:
        """
        Return all objects schemas from database; one if id is specified; None if object not found.
        """
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
                    return OrderSchema(id=result[0], user_id=result[1], food_id=result[2])
                return None
            return (
                [
                    OrderSchema(id=res[0], user_id=res[1], food_id=res[2])
                    for res in pre_result.all()
                ]
                if pre_result
                else None
            )
