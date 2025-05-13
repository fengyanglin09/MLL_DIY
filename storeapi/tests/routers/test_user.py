import pytest
from httpx import AsyncClient, Response


async def register_user(
    async_client: AsyncClient, username: str, email: str, password: str
) -> Response:
    response = await async_client.post(
        "/register", json={"username": username, "email": email, "password": password}
    )
    return response


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(async_client, "mark", "test@example.net", "1234")
    assert response.status_code == 201
    assert "User registered" in response.json()["message"]


@pytest.mark.anyio
async def test_register_user_already_exists(
    async_client: AsyncClient, registered_user: dict
):

    response = await register_user(
        async_client,
        registered_user["username"],
        registered_user["email"],
        registered_user["password"],
    )

    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]
