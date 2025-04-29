from pydantic import BaseModel


class TripInput(BaseModel):
    start: int
    end: int
    description: str
    car_id: int


class TripOutput(TripInput):
    id: int

    class Config:
        orm_mode = True
