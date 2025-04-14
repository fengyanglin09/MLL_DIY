from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def welcome():
    """Return a friendly welcome message"""
    return {'message' : f"Welcome, haha to the car sharing service!"}