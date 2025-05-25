

import pytest

from httpx import AsyncClient, Response
from fastapi import Request


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
    assert "User created" in response.json()["detail"]


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


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/token",
        data={"username": "test@example.net", "password": "1234"}
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_user(async_client: AsyncClient, confirmed_user: dict):
    response = await async_client.post(
        "/token",
        data={"username": confirmed_user["email"], "password": confirmed_user["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"



@pytest.mark.anyio
async def test_confirm_user(async_client: AsyncClient, mocker):
    spy = mocker.spy(Request, "url_for")
    await register_user(async_client, "mark", "test@example.net", "1234")
    confirmation_url = str(spy.spy_return)

    response = await async_client.get(confirmation_url)

    assert response.status_code == 200
    assert "User confirmed" in response.json()["detail"]



@pytest.mark.anyio
async def test_confirm_user_invalid_token(async_client: AsyncClient):
    response = await async_client.get("/confirm/invalidtoken")
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_user_not_confirmed(
    async_client: AsyncClient, registered_user: dict
):
    response = await async_client.post(
        "/token",
        data={"username": registered_user["email"], "password": registered_user["password"]},
    )
    assert response.status_code == 401
    assert "User is not confirmed" in response.json()["detail"]
