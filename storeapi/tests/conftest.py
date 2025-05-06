# storeapi/tests/conftest.py

import os
import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Set environment for test BEFORE any app import
os.environ["ENV_STATE"] = "test"

from storeapi.main import app
from storeapi.database import database


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
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
