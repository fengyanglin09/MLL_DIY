import logging

from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from storeapi.configs.security_conf import get_user
from storeapi.database.database import database, user_table
from storeapi.models.user import UserIn

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

    # todo hash password
    query = user_table.insert().values(
        username=user.username, email=user.email, password=user.password
    )

    logger.debug(query)

    await database.execute(query)
    return {"message": "User registered successfully"}
