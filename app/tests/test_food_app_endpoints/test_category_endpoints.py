import httpx
import pytest

from app.food.schemas import CategorySchema, CategorySchemaRead


@pytest.mark.asyncio
async def test_category_endp_all(get_client, prepare_category):
    client: httpx.AsyncClient = get_client
    r = await client.get("category/all/")
    assert r.status_code == 200
    assert CategorySchemaRead.model_validate(r.json()[0])


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_category_endp_by_id(id_, get_client, prepare_category):
    client: httpx.AsyncClient = get_client
    r = await client.get(f"category/{id_}/")
    assert r.status_code == 200
    assert CategorySchemaRead.model_validate(r.json())


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_category_endp_insert(id_, get_client, prepare_category):
    client: httpx.AsyncClient = get_client
    payload = CategorySchema(
        name=f"test-category-insert-{id_}",
    ).model_dump()
    r = await client.post(url="category/add/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get(url="category/all/")).json()
    assert r.json() == (await client.get(url=f"category/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_category_endp_update(id_, get_client, prepare_category):
    client: httpx.AsyncClient = get_client
    payload = CategorySchema(
        name=f"test-category-updated-{id_}",
    ).model_dump()
    r = await client.put(url=f"category/update/{id_}/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get("category/all/")).json()
    assert r.json() == (await client.get(f"category/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_category_endp_delete(id_, get_client, prepare_category):
    client: httpx.AsyncClient = get_client
    r = await client.delete(url=f"category/delete/{id_}/")
    assert r.status_code == 200
    assert r.json() not in (await client.get("category/all/")).json()
    assert None is (await client.get(f"category/{id_}/")).json()
