from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome():
    """Return a friendly welcome message"""
    return {'message' : "Welcom to the car sharing service!"}