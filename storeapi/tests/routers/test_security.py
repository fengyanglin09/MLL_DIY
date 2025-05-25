import pytest
import pytest_mock
from fastapi import HTTPException
from jose import jwt

from storeapi.configs.jwt_conf import (
    ALGORITHM,
    SECRET_KEY,
    access_token_expires,
    create_access_token,
    confirm_token_expires,
    create_confirmation_token,
)
from storeapi.configs.security_conf import (
    authenticate_user,
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
    get_subject_for_token_type,
)


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


def test_confirm_token_expire_minutes():
    assert confirm_token_expires() == 1440


def test_create_access_token():

    token = create_access_token("123")

    assert {"sub": "123", "type": "access"}.items() <= jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM]).items()


def test_create_confirmation_token():

    token = create_confirmation_token("123")

    assert {"sub": "123", "type": "confirmation"}.items() <= jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM]).items()



@pytest.mark.parametrize(
    "func,email,expected_type",
    [
        (create_access_token, "123", "access"),
        (create_access_token, "user@example.com", "access"),
        (create_confirmation_token, "123", "confirmation"),
        (create_confirmation_token, "user@example.com", "confirmation"),
    ],
)
def test_token_creation(func: callable, email: str, expected_type: str):
    token = func(email)
    decoded = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    assert {"sub": email, "type": expected_type}.items() <= decoded.items()

@pytest.mark.anyio
async def test_authenticate_user(confirmed_user: dict):

    user = await authenticate_user(confirmed_user["email"], confirmed_user["password"])

    assert user.email == confirmed_user["email"]
    assert verify_password(confirmed_user["password"], user.password)


@pytest.mark.anyio
async def test_authenticate_user_not_found(confirmed_user: dict):
    with pytest.raises(HTTPException):
        await authenticate_user("nonexist@example.net", "1234")


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(confirmed_user: dict):
    with pytest.raises(HTTPException):
        await authenticate_user(confirmed_user["email"], "wrongpassword")


@pytest.mark.anyio
async def test_get_current_user(confirmed_user: dict):
    token = create_access_token(confirmed_user["email"])
    user = await get_current_user(token)
    assert user.email == confirmed_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException):
        await get_current_user("invalidtoken")



@pytest.mark.anyio
async def test_get_current_user_wrong_type_token(confirmed_user: dict):
    token = create_confirmation_token(confirmed_user["email"])
    with pytest.raises(HTTPException):
        await get_current_user(token)

@pytest.mark.anyio
async def test_get_subject_for_token_type_valid_confirmation():
    email = "test@example.com"
    token = create_confirmation_token(email)
    subject = await get_subject_for_token_type(token, "confirmation")
    assert subject == email

@pytest.mark.anyio
async def test_get_subject_for_token_type_valid_access():
    email = "test@example.com"
    token = create_access_token(email)
    subject = await get_subject_for_token_type(token, "access")
    assert subject == email


@pytest.mark.anyio
async def test_get_subject_for_token_type_expired(mocker: pytest_mock.MockerFixture):
    mocker.patch("storeapi.configs.jwt_conf.access_token_expires", return_value=-1)
    email = "test@example.com"
    token = create_access_token(email)
    with pytest.raises(HTTPException) as exc_info:
        await get_subject_for_token_type(token, "access")

    assert "Token has expired"  in str(exc_info.value.detail)


@pytest.mark.anyio
async def test_get_subject_for_token_type_invalid_token():
    token = "invalid token"
    with pytest.raises(HTTPException) as exc_info:
        await get_subject_for_token_type(token, "access")

    assert "Invalid token" in str(exc_info.value.detail)


@pytest.mark.anyio
async def test_get_subject_for_token_type_missing_sub():
    email = "test@example.com"
    token = create_access_token(email)
    payload = jwt.decode(
        token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    del payload["sub"]

    token = jwt.encode(
        payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_subject_for_token_type(token, "access")
    assert "Token is missing 'sub' field" in str(exc_info.value.detail)


@pytest.mark.anyio
async def test_get_subject_for_token_type_wrong_type():
    email = "test@example.com"
    token = create_confirmation_token(email)

    with pytest.raises(HTTPException) as exc_info:
        await get_subject_for_token_type(token, "access")

    assert "Token is not of type 'access'" in str(exc_info.value.detail)