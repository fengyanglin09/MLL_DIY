import pytest
from httpx import AsyncClient

from storeapi.database.database import database, user_table


@pytest.fixture(scope="function")
async def registered_user(async_client: AsyncClient) -> dict:
    user_detail = {"username": "mark", "email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_detail)
    query = user_table.select().where(user_table.c.email == user_detail["email"])
    user = await database.fetch_one(query)
    user_detail["id"] = user.id
    return user_detail


@pytest.fixture(scope="function")
async def confirmed_user(registered_user: dict) -> dict:

    updateQuery =(
        user_table.update().where(user_table.c.email == registered_user["email"])
        .values(confirmed=True)
    )
    await database.execute(updateQuery)
    registered_user["confirmed"] = True
    return registered_user