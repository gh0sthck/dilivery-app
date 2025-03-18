from typing import Optional

from sqlalchemy import Insert, Select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import async_session
from app.auth.models import User
from app.auth.schemas import SRegisterUser, SUser
from app.db_explorer import DbExplorer


class UserExplorer(DbExplorer):
    def __init__(self) -> None:
        super().__init__(model=User, schema=SUser)

    @DbExplorer._log
    async def get_by_username(
        self, username: str, _session: AsyncSession = async_session()
    ) -> Optional[SUser]:
        async with _session as session:
            query = Select(self.model).where(User.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            self.logger.info(f"Result by username = {username}")
            if user:
                return SUser.model_validate(obj=user, from_attributes=True)
            return None

    @DbExplorer._log
    async def post(
        self,
        schema: SRegisterUser,
        role_id: int = 0,
        _session: AsyncSession = async_session(),
    ) -> SUser:
        """Return object schema, which will added to database."""
        async with _session as session:
            s = schema.model_dump()
            s["role"] = role_id
            query = Insert(self.model).values(s)
            q = await session.execute(query)
            pk = q.inserted_primary_key[0]
            s["id"] = pk
            await session.commit()
        return self.schema.model_validate(s)
