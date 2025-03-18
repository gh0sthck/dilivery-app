import httpx
import pytest

from app.food.schemas import FoodSchema, FoodSchemaRead


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
    assert FoodSchemaRead.model_validate(r.json())


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_food_endp_insert(id_, get_client, prepare_food):
    client: httpx.AsyncClient = get_client
    payload = FoodSchema(
        name=f"test-food-insert-{id_}",
        rate=0.0 + id_,
        description="testfood",
        price=id_,
        shop=id_ + 10,
        category=id_ + 10,
    ).model_dump()
    r = await client.post(url="food/add/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get(url="food/all/")).json()
    assert r.json() == (await client.get(url=f"food/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_food_endp_update(id_, get_client, prepare_food):
    client: httpx.AsyncClient = get_client
    payload = FoodSchema(
        name=f"test-food-updated-{id_}",
        rate=0.0 + id_,
        description="testfoodupdated",
        price=id_,
        shop=id_,
        category=id_,
    ).model_dump()
    r = await client.put(url=f"food/update/{id_}/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get("food/all/")).json()
    assert r.json() == (await client.get(f"food/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_food_endp_delete(id_, get_client, prepare_food):
    client: httpx.AsyncClient = get_client
    r = await client.delete(url=f"food/delete/{id_}/")
    assert r.status_code == 200
    assert r.json() not in (await client.get("food/all/")).json()
    assert None is (await client.get(f"food/{id_}/")).json()
