from pydantic import BaseModel


class CarInput(BaseModel):
    size: str
    fuel: str = "electric"
    doors: int
    transmission: str = "auto"


class CarOutput(CarInput):
    id: int

    class Config:
        orm_mode = True
