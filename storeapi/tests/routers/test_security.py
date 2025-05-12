import pytest
from httpx import AsyncClient

from storeapi.configs.security_conf import get_user

from storeapi.database.database import user_table, database


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_detail = {"username":"mark", "email":"test@example.net", "password":"1234"}
    await async_client.post("/register", json=user_detail)
    query = user_table.select().where(user_table.c.email == user_detail["email"])
    user = await database.fetch_one(query)
    user_detail["id"] = user.id
    return user_detail




@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await get_user(registered_user["email"])

    assert user.email == registered_user["email"]



@pytest.mark.anyio
async def test_get_user_not_found():
    user = await get_user("nonexist@example.com")
    assert user is None