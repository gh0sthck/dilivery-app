import httpx
import pytest
import pytest_asyncio

from app.database import get_async_session
from app.food.schemas import FoodSchemaRead
from app.tests.models import get_test_session
from main import app

BASE_URL = "http://localhost:8000/api/"


@pytest_asyncio.fixture
async def get_client():
    app.dependency_overrides[get_async_session] = get_test_session
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=BASE_URL
    ) as cli:
        yield cli


@pytest.mark.asyncio
async def test_food_endp_all(get_client, prepare_food):
    client: httpx.AsyncClient = get_client
    r = await client.get("food/all/")
    assert r.status_code == 200
    assert FoodSchemaRead.model_validate(r.json()[0])


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_food_endp_by_id(id_, get_client, prepare_food):
    client: httpx.AsyncClient = get_client
    r = await client.get(f"food/{id_}/")
    assert r.status_code == 200
    print(r.json()) 
    assert FoodSchemaRead.model_validate(r.json())
