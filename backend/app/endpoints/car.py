from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params, paginate
from typing import Optional

from database import get_db
from schemas import Car, CarCard, CarCreate, CarUpdate, CarDetailed
import crud

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/", response_model=Page[Car])
def get_all_cars(
    db: Session = Depends(get_db),
    params: Params = Depends(),  # ✅ обязательно
    brand_id: Optional[int] = None,
    model_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_mileage: Optional[int] = None,
    max_mileage: Optional[int] = None,
    min_engine_capacity: Optional[float] = None,
    max_engine_capacity: Optional[float] = None,
    min_engine_power: Optional[int] = None,
    max_engine_power: Optional[int] = None,
    min_latitude: Optional[float] = None,
    max_latitude: Optional[float] = None,
    min_longitude: Optional[float] = None,
    max_longitude: Optional[float] = None,
    color: Optional[str] = None,
    drive_type: Optional[str] = None,
    transmission: Optional[str] = None,
    fuel_type: Optional[str] = None,
    steering_side: Optional[str] = None,
    car_condition: Optional[str] = None,
    is_sold: Optional[bool] = None,
    body_type: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc"
):
    filters = {
        "brand_id": brand_id,
        "model_id": model_id,
        "is_sold": is_sold,
        "body_type": body_type,
    }

    # Фильтры с диапазонами
    if min_price is not None or max_price is not None:
        filters["price"] = (min_price, max_price)
    if min_year is not None or max_year is not None:
        filters["year"] = (min_year, max_year)
    if min_mileage is not None or max_mileage is not None:
        filters["mileage"] = (min_mileage, max_mileage)
    if min_engine_capacity is not None or max_engine_capacity is not None:
        filters["engine_capacity"] = (min_engine_capacity, max_engine_capacity)
    if min_engine_power is not None or max_engine_power is not None:
        filters["engine_power"] = (min_engine_power, max_engine_power)
    if min_latitude is not None or max_latitude is not None:
        filters["latitude"] = (min_latitude, max_latitude)
    if min_longitude is not None or max_longitude is not None:
        filters["longitude"] = (min_longitude, max_longitude)
    # Фильтры с точными значениями
    if color is not None:
        filters["color"] = color
    if drive_type is not None:  
        filters["drive_type"] = drive_type
    if transmission is not None:
        filters["transmission"] = transmission
    if fuel_type is not None:
        filters["fuel_type"] = fuel_type
    if steering_side is not None:
        filters["steering_side"] = steering_side
    if car_condition is not None:
        filters["car_condition"] = car_condition
    # Удаляем фильтры со значением None

    filters = {k: v for k, v in filters.items() if v is not None}
    return crud.get_all_cars_paginated(db, filters, sort_by, sort_order, params=params)

@router.get("/cards", response_model=Page[CarCard])
def get_car_cards(params: Params = Depends(), db: Session = Depends(get_db)):
    query = crud.get_car_cards_query(db)
    return paginate(query, params)

@router.get("/{car_id}", response_model=CarDetailed)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.post("/", response_model=Car)
def create_car(car: CarCreate, db: Session = Depends(get_db), user_id: int = 1):
    return crud.create_car(db, car, user_id)

@router.put("/{car_id}", response_model=Car)
def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    return crud.update_car(db, car_id, car)

@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    if not crud.delete_car(db, car_id):
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}
