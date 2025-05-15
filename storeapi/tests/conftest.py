# storeapi/tests/conftest.py

import os

os.environ["ENV_STATE"] = "test"

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from storeapi.database.database import database
from storeapi.main import app

from storeapi.tests.user_fixtures import registered_user # noqa: F401


@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def async_client(client) -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac


@pytest.fixture(autouse=True)
async def db_transaction():
    # Ensure DB is connected
    if not database.is_connected:
        await database.connect()

    async with database.transaction(force_rollback=True):
        yield

    # All changes in test rolled back automatically

@pytest.fixture(scope="function")
async def logged_in_token(async_client: AsyncClient, registered_user: dict) -> str:  # noqa: F811
    response = await async_client.post(
        "/token",
        data={"username": registered_user["email"], "password": registered_user["password"]}

    )
    return response.json()["access_token"]