from contextlib import asynccontextmanager

from fastapi import FastAPI
from routers import car_api, welcome_api
from backend.db.init_db import init_db
# import uvicorn





@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(car_api.router)
app.include_router(welcome_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

