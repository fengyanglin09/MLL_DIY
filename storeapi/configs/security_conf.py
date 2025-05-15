import logging

from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from storeapi.database.database import database, user_table

from storeapi.configs.jwt_conf import (
    credentials_exception,
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,
)

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



async def get_user(email: str):
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
        raise credentials_exception
    if not verify_password(password, user["password"]):
        raise credentials_exception
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.debug("Getting current user from token: %s", token)

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except JWTError as e:
        raise credentials_exception from e

    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user