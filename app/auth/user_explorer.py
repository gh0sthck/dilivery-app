from typing import Optional

from sqlalchemy import Insert, Select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import async_session
from app.auth.models import User
from app.auth.schemas import SRegisterUser, SUser, SUserView
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
                return SUser.model_validate(obj=user, from_attributes=True)
            return None

    async def post(self, schema: SRegisterUser) -> SUser:
        """Return object schema, which be added to database."""
        session: AsyncSession
        async with async_session() as session:
            s = schema.model_dump()
            s["role"] = 0 
            query = Insert(self.model).values(s)
            q = await session.execute(query)
            pk = q.inserted_primary_key[0]
            s["id"] = pk
            await session.commit()
        return self.schema.model_validate(s)
