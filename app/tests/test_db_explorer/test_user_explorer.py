import pytest

from app.auth.schemas import SRegisterUser, SUser
from app.auth.user_explorer import UserExplorer
from app.tests.conftest import test_async_session


explorer = UserExplorer(session=test_async_session())


@pytest.mark.asyncio
@pytest.mark.parametrize("username", [f"test-user-{cnt}" for cnt in range(10, 20)])
async def test_by_username_users(username, prepare_users):
    result = await explorer.get_by_username(username=username)
    assert isinstance(result, SUser)
    assert result.username == username


@pytest.mark.asyncio
@pytest.mark.parametrize("id_", [i for i in range(9)])
async def test_post_users(id_, prepare_users):
    payload = SRegisterUser(
        username=f"test-user-reg-{id_}",
        full_name=f"test-name-{id_}",
        email=f"testregemail{id_}@gmail.com",
        password=f"testpass-{id_}",
        city=id_+10,
    )
    result = await explorer.post(payload, 10)
    assert isinstance(result, SUser)
