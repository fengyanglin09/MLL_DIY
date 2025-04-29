from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .car import Car


class Trip(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    start: int
    end: int
    description: str
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")
