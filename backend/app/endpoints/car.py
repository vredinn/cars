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
    is_sold: Optional[bool] = None,
    body_type: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc"
):
    filters = {
        "brand_id": brand_id,
        "model_id": model_id,
        "min_price": min_price,
        "max_price": max_price,
        "is_sold": is_sold,
        "body_type": body_type,
    }
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
