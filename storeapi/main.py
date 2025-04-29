from fastapi import FastAPI

from storeapi.routers.post import router as post_router

app = FastAPI()

app.include_router(post_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
