from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine

from .settings import config


engine: AsyncEngine = create_async_engine(url=config.database.dsn)
async_session: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"<Model: {self.id}>"


async def get_async_session():
    async with async_session() as sess:
        yield sess
