from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi_pagination import Page, Params, paginate
from typing import Dict, List, Optional
from uuid import UUID
from database import get_db
from schemas import Car, CarCard, CarCreate, CarUpdate, CarDetailed
import crud
from enum import Enum

# Модели Enum
from models import DriveTypeEnum, TransmissionEnum, FuelTypeEnum, SteeringSideEnum, CarConditionEnum, BodyTypeEnum

router = APIRouter(prefix="/cars", tags=["Cars"])

def get_enum_value(enum_class: Enum, value: str) -> Enum:
    try:
        return enum_class(value)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Неверное значение для {enum_class.__name__}: {value}")

@router.get("/popular", response_model=List[CarCard])
def get_popular_cars(db: Session = Depends(get_db)):
    return crud.get_most_popular_cars(db)

@router.get("/", response_model=Page[CarCard])
def get_all_cars(
    db: Session = Depends(get_db),
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
    sort_order: Optional[str] = "desc",    
    page: int = Query(1, ge=1, description="Номер страницы (начиная с 1)"),    
    size: int = Query(5, include_in_schema=False, ge=1, le=100),
):
    params = Params(page=page, size=5)  # Устанавливаем size=5 для фиксированного пагинации
    filters = build_filters(
        brand_id, model_id, min_price, max_price, min_year, max_year,
        min_mileage, max_mileage, min_engine_capacity, max_engine_capacity,
        min_engine_power, max_engine_power, min_latitude, max_latitude,
        min_longitude, max_longitude, color, drive_type, transmission,
        fuel_type, steering_side, car_condition, is_sold, body_type
    )

    # Удаляем фильтры со значением None
    filters = {k: v for k, v in filters.items() if v is not None}

    try:
        return crud.get_all_cars_paginated(db, filters, sort_by, sort_order, params=params)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))


@router.get("/user_cars/{user_uuid}", response_model=Page[CarCard])
def get_user_cars(user_uuid: UUID, db: Session = Depends(get_db), page: int = Query(1, ge=1), size: int = Query(5, ge=1)):
    params = Params(page=page, size=5) 
    return crud.get_user_cars_paginated(db, user_uuid, params=params)


def build_filters(
    brand_id, model_id, min_price, max_price, min_year, max_year,
    min_mileage, max_mileage, min_engine_capacity, max_engine_capacity,
    min_engine_power, max_engine_power, min_latitude, max_latitude,
    min_longitude, max_longitude, color, drive_type, transmission,
    fuel_type, steering_side, car_condition, is_sold, body_type
) -> Dict:
    filters = {
        "brand_id": brand_id,
        "model_id": model_id,
        "is_sold": is_sold,
        "body_type": body_type,
    }

    # Добавляем фильтры с диапазонами
    add_range_filter(filters, "price", min_price, max_price)
    add_range_filter(filters, "year", min_year, max_year)
    add_range_filter(filters, "mileage", min_mileage, max_mileage)
    add_range_filter(filters, "engine_capacity", min_engine_capacity, max_engine_capacity)
    add_range_filter(filters, "engine_power", min_engine_power, max_engine_power)
    add_range_filter(filters, "latitude", min_latitude, max_latitude)
    add_range_filter(filters, "longitude", min_longitude, max_longitude)

    # Добавляем точные фильтры с Enum-переводом
    if drive_type:
        filters["drive_type"] = get_enum_value(DriveTypeEnum, drive_type)
    if transmission:
        filters["transmission"] = get_enum_value(TransmissionEnum, transmission)
    if fuel_type:
        filters["fuel_type"] = get_enum_value(FuelTypeEnum, fuel_type)
    if steering_side:
        filters["steering_side"] = get_enum_value(SteeringSideEnum, steering_side)
    if car_condition:
        filters["car_condition"] = get_enum_value(CarConditionEnum, car_condition)

    # Добавляем точные фильтры для строковых значений
    add_exact_filter(filters, "color", color)

    return filters

def add_range_filter(filters, field, min_value, max_value):
    if min_value is not None or max_value is not None:
        filters[field] = (min_value, max_value)

def add_exact_filter(filters, field, value):
    if value is not None:
        filters[field] = value

@router.get("/id_{car_id}", response_model=CarDetailed)
def get_car_by_id(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@router.get("/{car_uuid}", response_model=CarDetailed)
def get_car_by_uuid(car_uuid: UUID, db: Session = Depends(get_db)):
    car = crud.get_car_by_uuid(db, car_uuid)
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
