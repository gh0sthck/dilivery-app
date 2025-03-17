from typing import Optional

from sqlalchemy import Select, Update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.schemas import SUser
from app.database import async_session


async def change_create_status(user_id: int) -> Optional[SUser]:
    session: AsyncSession
    async with async_session() as session:
        user_query = Select(User).where(User.id == user_id)
        pre_result = await session.execute(user_query)
        user: Optional[User] = pre_result.scalar_one_or_none()
        if user:
            new_model = SUser.model_validate(user.__dict__)
            if new_model.order_create:
                new_model.order_create = False
            else:
                new_model.order_create = True
            query = Update(User).where(User.id == user_id).values(new_model.model_dump())
            await session.execute(query)
            await session.commit()
            return new_model
        return None
