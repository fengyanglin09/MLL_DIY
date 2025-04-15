from fastapi import HTTPException
from sqlmodel import select, Session

from backend.models.car import Car


def get_all_cars(db: Session, size: str | None = None, doors: int | None = None) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return db.exec(query).all()


def get_car_by_id(db: Session, id: int) -> Car:
    car = db.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"Car not found {id}")



def add_car(db: Session, car: Car) -> Car:
    new_car = car.model_validate(car)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


def update_car(db: Session, id: int, new_data: Car) -> Car:
    car = db.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        db.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id = {id}.")


def delete_car(db: Session, id: int) -> None:
    car = db.get(Car, id)
    if car:
        db.delete(car)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car found")