

from fastapi import APIRouter, Depends
from backend.db.database import get_db
from sqlmodel import Session
from backend.services import car_service
from backend.models.car import Car

router = APIRouter(prefix="/api")

@router.get("/cars")
async def get_cars(db: Session = Depends(get_db), size: str | None = None, doors: int | None = None) -> list:
    return car_service.get_all_cars(db, size, doors)


@router.get("/cars/{id}")
def car_by_id(id: int, db: Session = Depends(get_db)) -> Car:
    return car_service.get_car_by_id(db, id)


@router.post("car")
def add_car(new_car: Car, db: Session = Depends(get_db)) -> Car:
    return car_service.add_car(db, new_car)

@router.put("/car/{id}")
def change_car(id: int, new_data: Car, db: Session = Depends(get_db) ) -> Car:
    return car_service.update_car(db, id, new_data)


@router.delete("/car/{id}", status_code=204)
def remove_car(id: int, db: Session = Depends(get_db)) -> None:
    car_service.delete_car(db, id)

