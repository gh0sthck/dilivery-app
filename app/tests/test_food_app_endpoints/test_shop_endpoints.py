import httpx
import pytest

from app.food.schemas import ShopSchema, ShopSchemaRead


@pytest.mark.asyncio
async def test_shop_endp_all(get_client, prepare_shop):
    client: httpx.AsyncClient = get_client
    r = await client.get("shop/all/")
    assert r.status_code == 200
    assert ShopSchemaRead.model_validate(r.json()[0])


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_shop_endp_by_id(id_, get_client, prepare_shop):
    client: httpx.AsyncClient = get_client
    r = await client.get(f"shop/{id_}/")
    assert r.status_code == 200
    assert ShopSchemaRead.model_validate(r.json())


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(1, 10)])
async def test_shop_endp_insert(id_, get_client, prepare_shop):
    client: httpx.AsyncClient = get_client
    payload = ShopSchema(
        name=f"test-shop-insert-{id_}",
        rate=0.0 + id_,
        city=id_ + 10,
    ).model_dump()
    r = await client.post(url="shop/add/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get(url="shop/all/")).json()
    assert r.json() == (await client.get(url=f"shop/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_shop_endp_update(id_, get_client, prepare_shop):
    client: httpx.AsyncClient = get_client
    payload = ShopSchema(
        name=f"test-shop-updated-{id_}",
        rate=0.0 + id_,
        city=id_,
    ).model_dump()
    r = await client.put(url=f"shop/update/{id_}/", json=payload)
    assert r.status_code == 200
    assert r.json() in (await client.get("shop/all/")).json()
    assert r.json() == (await client.get(f"shop/{id_}/")).json()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_shop_endp_delete(id_, get_client, prepare_shop):
    client: httpx.AsyncClient = get_client
    r = await client.delete(url=f"shop/delete/{id_}/")
    assert r.status_code == 200
    assert r.json() not in (await client.get("shop/all/")).json()
    assert None is (await client.get(f"shop/{id_}/")).json()
