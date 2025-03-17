import pytest

from app.db_explorer import DbExplorer
from app.tests.models import ModelTest, ModelTestS
from app.tests.conftest import test_async_session

test_explorer = DbExplorer(ModelTest, ModelTestS, session=test_async_session())


@pytest.mark.asyncio
async def test_get_all(prepare_test_model):
    result = await test_explorer.get()
    assert isinstance(result, list)
    assert isinstance(result[0], ModelTestS)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [
    i for i in range(10, 20) 
])
async def test_get_by_id(id_, prepare_test_model):
    result = await test_explorer.get(id_)
    assert isinstance(result, ModelTestS) 


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10)])
async def test_insert(id_, prepare_test_model):
    payload = ModelTestS(
        id=id_,
        value=f"test-value-{id_}"
    )
    result = await test_explorer.post(payload)
    assert result == payload
    assert result in await test_explorer.get()
    assert result == await test_explorer.get(id=id_)


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_update(id_, prepare_test_model):
    payload = ModelTestS(
        id=id_,
        value=f"test-value-updated-{id_}" 
    ) 
    result = await test_explorer.update(id=id_, schema=payload)
    assert result == payload
    assert result == await test_explorer.get(id=id_)
    assert result in await test_explorer.get()


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(10, 20)])
async def test_delete(id_, prepare_test_model):
    result = await test_explorer.delete(id=id_)
    assert isinstance(result, ModelTestS)
    assert result not in await test_explorer.get()
    assert await test_explorer.get(id=id_) is None 
