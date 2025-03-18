# from logging import config

from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Model

from app.settings import config
 
test_engine = create_async_engine(url=config.tests.db_dsn)
Model.metadata.bind = test_engine
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)

class ModelTest(Model):
    __tablename__ = "testmodel"
    value: Mapped[str] = mapped_column(String(length=80))


class ModelTestS(BaseModel):
    id: int
    value: str


async def get_test_session():
    async with test_async_session() as session:
        yield session
