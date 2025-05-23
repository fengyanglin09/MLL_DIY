import datetime
import logging
from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

"""
this is to define the endpoint for the user to get the token with username and password
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "your_secret_key"

ALGORITHM = "HS256"


def create_credentials_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )



def access_token_expires() -> int:
    return 30

def confirm_token_expires() -> int:
    return 1440 # 24 hours

logger = logging.getLogger(__name__)

def create_access_token(email: str):
    logger.debug("Creating access token for email: %s", email, extra={"email": email})
    expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=access_token_expires())
    jwt_data = {
        "sub": email,
        "exp": expire,
        "type": "access",
    }
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_confirmation_token(email: str):
    logger.debug("Creating confirmation token for email: %s", email, extra={"email": email})
    expire = datetime.datetime.now(datetime.UTC) + timedelta(minutes=confirm_token_expires())
    jwt_data = {
        "sub": email,
        "exp": expire,
        "type": "confirmation",
    }
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt