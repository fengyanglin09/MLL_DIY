import logging

from fastapi import APIRouter, HTTPException, status
from storeapi.models.user import User, UserIn
from storeapi.configs.security_conf import get_user
from storeapi.database.database import database, user_table


router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/register", status_code=201)
async def register(user: UserIn):
    """
    Register a new user.
    """
    # Here you would typically hash the password and save the user to the database
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    #todo hash password
    query = user_table.insert().values(username = user.username, email = user.email, password = user.password)

    logger.debug(query)

    await database.execute(query)
    return {"message": "User registered successfully"}