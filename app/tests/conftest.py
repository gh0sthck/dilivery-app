import asyncio
from typing import Iterable

import pytest

import pytest_asyncio
from sqlalchemy import Delete, Insert
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from app.city.models import City
from app.food.models import Category, Food, Shop
from app.settings import config
from app.database import Model
from fixtures import get_city_list, get_category_list, get_shop_list, get_food_list


test_engine = create_async_engine(url=config.tests.db_dsn)
test_async_session = async_sessionmaker(bind=test_engine, expire_on_commit=True)
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


async def delete_tables(table: Model):
    async with test_async_session() as session:
        await session.execute(Delete(table))
        await session.commit()


async def create_tables(table: Model, values: Iterable):
    await delete_tables(table)
    async with test_async_session() as session:
        await session.exeucte(Insert(table).values(values))
        await session.commit()


@pytest_asyncio.fixture
async def prepare_city(get_city_list):
    await create_tables(City, get_city_list)
    yield
    await delete_tables(City)


@pytest_asyncio.fixture
async def prepare_category(get_category_list):
    await create_tables(Category, get_category_list)
    yield
    await delete_tables(Category)


@pytest_asyncio.fixture
async def prepare_shop(get_shop_list):
    await create_tables(Shop, get_shop_list)
    yield
    await delete_tables(Shop)


@pytest_asyncio.fixture
async def prepare_food(prepare_category, prepare_shop, get_food_list):
    await create_tables(Food, get_food_list)
    yield
    await delete_tables(Food)
