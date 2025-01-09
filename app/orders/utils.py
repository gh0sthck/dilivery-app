from typing import Optional
from sqlalchemy import Select, Update
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.schemas import SOrder
from app.database import async_session
from app.orders.models import Order


async def change_order_status(order_id: int, status: int) -> Optional[SOrder]:
    session: AsyncSession
    async with async_session() as session:
        query = Select(Order).where(Order.id == order_id)
        pre_result = await session.execute(query)
        order = pre_result.scalar_one_or_none()
        if order:
            new_model = SOrder.model_validate(order.__dict__)
            new_model.status = status
            update_query = (
                Update(Order).where(Order.id == order_id).values(new_model.model_dump())
            )
            await session.execute(update_query)
            await session.commit()
            return new_model
        return None
