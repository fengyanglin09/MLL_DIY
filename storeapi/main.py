# storeapi/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI

from storeapi.database import database
from storeapi.routers.post import router as post_router
from storeapi.config import get_config


@asynccontextmanager
async def lifespan(app: FastAPI):
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
