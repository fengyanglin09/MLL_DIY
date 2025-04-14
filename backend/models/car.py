from typing import TYPE_CHECKING, ClassVar
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .trip import Trip

class Car(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    trips: list["Trip"] = Relationship(back_populates="car")
