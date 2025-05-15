import logging

from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from storeapi.configs.jwt_conf import create_access_token
from storeapi.configs.security_conf import get_user, authenticate_user
from storeapi.database.database import database, user_table
from storeapi.models.user import UserIn

from storeapi.configs.security_conf import get_password_hash, get_user

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn):
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
    return {"message": "User registered successfully"}


@router.post("/token")
async def login(user: UserIn):
    """
    Login a user and return a token.
    """
    # Here you would typically verify the password and return a token
    db_user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(db_user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }