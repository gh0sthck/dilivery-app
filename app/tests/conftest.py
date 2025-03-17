import asyncio

import pytest

from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from settings import config
from database import Model


test_engine = create_async_engine(url=config.tests.db_dsn)
test_async_session = async_sessionmaker(
    bind=test_engine, expire_on_commit=True
)
Model.metadata.bind = test_engine


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    async with test_engine.begin() as connect:
        await connect.run_sync(Model.metadata.create_all)
    yield
    async with test_engine.begin() as connect:
        await connect.run_sync(Model.metadata.drop_all)
