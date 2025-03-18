import httpx
import pytest

from app.city.schema import CitySchema, CitySchemaRead


@pytest.mark.asyncio
async def test_city_endp_all(get_client, prepare_city):
    client: httpx.AsyncClient = get_client
    r = await client.get("city/all/")
    assert r.status_code == 200
    assert CitySchemaRead.model_validate(r.json()[0])


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_city_endp_by_id(id_, get_client, prepare_city):
    client: httpx.AsyncClient = get_client
    r = await client.get(f"city/{id_}/")
    assert r.status_code == 200
    assert CitySchemaRead.model_validate(r.json())


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_city_endp_insert(id_, get_client, prepare_city):
    client: httpx.AsyncClient = get_client
    payload = CitySchema(
        name=f"test-city-insert-{id_}",
    ).model_dump()
    r = await client.post(url="city/add/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get(url="city/all/")).json()
    assert r.json() == (await client.get(url=f"city/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_city_endp_update(id_, get_client, prepare_city):
    client: httpx.AsyncClient = get_client
    payload = CitySchema(
        name=f"test-city-updated-{id_}",
    ).model_dump()
    r = await client.put(url=f"city/update/{id_}/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get("city/all/")).json()
    assert r.json() == (await client.get(f"city/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_city_endp_delete(id_, get_client, prepare_city):
    client: httpx.AsyncClient = get_client
    r = await client.delete(url=f"city/delete/{id_}/")
    assert r.status_code == 200
    assert r.json() not in (await client.get("city/all/")).json()
    assert None is (await client.get(f"city/{id_}/")).json()

