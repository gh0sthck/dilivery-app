from typing import Optional

from sqlalchemy import Select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import async_session
from app.auth.models import User
from app.auth.schemas import SUser
from app.db_explorer import DbExplorer


class UserExplorer(DbExplorer):
    def __init__(self) -> None:
        super().__init__(model=User, schema=SUser) 

    async def get_by_username(self, username: str) -> Optional[SUser]:
        session: AsyncSession
        async with async_session() as session:
            query = Select(self.model).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user: 
                return SUser.model_validate(obj=user.__dict__) 
            return None
