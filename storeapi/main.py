# storeapi/main.py
import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from storeapi.app_conf import get_config
from storeapi.configs.logging_conf import configure_logging
from storeapi.database.database import database
from storeapi.routers.post import router as post_router
from storeapi.routers.user import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    # logger.debug("Hello World")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


"""
Yes, with the current setup, the X-Correlation-ID header will be included in the requests if the client provides it. 
If the client does not include this header, the CorrelationIdMiddleware will generate a new UUID and use it as the correlation ID for the request. 
This correlation ID will then be available for logging and other purposes throughout the request lifecycle.
"""

app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Correlation-ID",  # Set your custom header name here
)

app.include_router(post_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.status_code} {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )
    # return await request.app.default_exception_handler(request, exc)


if __name__ == "__main__":
    import uvicorn

    config = get_config()
    print("Running with config:", config.ENV_STATE)
    uvicorn.run("storeapi.main:app", host="127.0.0.1", port=8000, reload=True)
