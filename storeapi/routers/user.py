import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from storeapi.configs.jwt_conf import create_access_token, create_confirmation_token
from storeapi.configs.security_conf import (
    authenticate_user,
    get_password_hash,
    get_user,
    get_subject_for_token_type,
)
from storeapi.database.database import database, user_table
from storeapi.models.user import UserIn

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn, request: Request):
    """
    Register a new user.
    """
    # Here you would typically hash the password and save the user to the database
    try:
        if await get_user(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    hashed_password = get_password_hash(user.password)

    query = user_table.insert().values(
        username=user.username, email=user.email, password=hashed_password
    )

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created, Please confirm your email",
            "confirmation_url": request.url_for(
                "confirm_email",
                token=create_confirmation_token(user.email),
            )
            }


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login a user and return a token.
    """
    # Here you would typically verify the password and return a token
    db_user = await authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(db_user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/confirm/{token}")
async def confirm_email(token: str):
    """
    Confirm a user's email address.
    """
    email = get_subject_for_token_type(token, "confirmation")

    query = (
        user_table.update()
        .where(user_table.c.email == email)
        .values(confirmed=True)
    )

    logger.debug(query)

    await database.execute(query)

    return {"detail": "User confirmed successfully"}


