# storeapi/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from storeapi.database import database
from storeapi.routers.post import router as post_router
from storeapi.config import get_config

from storeapi.logging_conf import configure_logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Hello World")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)

if __name__ == "__main__":
    import uvicorn
    config = get_config()
    print("Running with config:", config.ENV_STATE)
    uvicorn.run("storeapi.main:app", host="127.0.0.1", port=8000, reload=True)


