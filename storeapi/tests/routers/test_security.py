import pytest
from fastapi import HTTPException
from jose import jwt

from storeapi.configs.jwt_conf import (ALGORITHM, SECRET_KEY,
                                       access_token_expires,
                                       create_access_token)
from storeapi.configs.security_conf import (authenticate_user,
                                            get_current_user,
                                            get_password_hash, get_user,
                                            verify_password)


def test_password_hash():
    password = "1234"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert verify_password(password, hashed_password)

@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await get_user(registered_user["email"])

    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await get_user("nonexist@example.com")
    assert user is None


def test_access_token_expire_minutes():
    assert access_token_expires() == 30


def test_create_access_token():

    token = create_access_token("123")

    assert {"sub": "123"}.items() <= jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM]).items()



@pytest.mark.anyio
async def test_authenticate_user(registered_user: dict):

    user = await authenticate_user(registered_user["email"], registered_user["password"])

    assert user.email == registered_user["email"]
    assert verify_password(registered_user["password"], user.password)


@pytest.mark.anyio
async def test_authenticate_user_not_found(registered_user: dict):
    with pytest.raises(HTTPException):
        await authenticate_user("nonexist@example.net", "1234")


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(HTTPException):
        await authenticate_user(registered_user["email"], "wrongpassword")


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = create_access_token(registered_user["email"])
    user = await get_current_user(token)
    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException):
        await get_current_user("invalidtoken")
