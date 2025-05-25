import logging
from typing import Annotated, Literal

from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from storeapi.configs.jwt_conf import (
    ALGORITHM,
    SECRET_KEY,
    oauth2_scheme,
    create_credentials_exception,
)
from storeapi.database.database import database, user_table
from storeapi.models.user import User

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



async def get_user(email: str) -> User | None:
    logger.debug("Fetching user with email: %s", email, extra={"email": email})

    query = user_table.select().where(user_table.c.email == email)

    result = await database.fetch_one(query)

    if result:
        logger.debug("User found: %s", result)
        return result
    return None


async def authenticate_user(email: str, password: str):
    logger.debug("Authenticating user with email: %s", email, extra={"email": email})
    user = await get_user(email)
    if not user:
        raise create_credentials_exception("Invalid email or password")
    if not verify_password(password, user["password"]):
        raise create_credentials_exception("Invalid email or password")
    if not user.confirmed:
        raise create_credentials_exception("User is not confirmed")
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.debug("Getting current user from token: %s", token)

    email = await get_subject_for_token_type(token, "access")

    user = await get_user(email=email)
    if user is None:
        raise create_credentials_exception("could not find user for this token")
    return user


async def get_subject_for_token_type(token: str, type: Literal["access", "confirmation"] = "access") -> str:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

    except ExpiredSignatureError as e:
        raise create_credentials_exception(
            "Token has expired",
        ) from e
    except JWTError as e:
        raise create_credentials_exception("Invalid token") from e

    email = payload.get("sub")
    if email is None:
        raise create_credentials_exception("Token is missing 'sub' field")

    token_type = payload.get("type")

    if token_type is None or token_type != type:
        raise create_credentials_exception(f"Token is not of type '{type}'")

    return email