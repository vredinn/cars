from typing import Optional
from sqlalchemy.orm import Session, selectinload
from uuid import uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import and_, asc, desc
from pathlib import Path

import models as m
from schemas import (
    CarCreate, CarUpdate
)

# ================ Car CRUD ================
def get_car(db: Session, car_id: int):
    return db.query(m.Car).options(selectinload(m.Car.images)).filter(m.Car.id == car_id).first()

def get_all_cars_paginated(
    db: Session,
    filters: dict,
    sort_by: Optional[str],
    sort_order: str,
    params: Params
):
    q = db.query(m.Car)

    # Обработка фильтров
    for attr, value in filters.items():
        if hasattr(m.Car, attr):
            column = getattr(m.Car, attr)
            if isinstance(value, tuple) and len(value) == 2:  # Диапазоны, например, min и max
                min_value, max_value = value
                if min_value is not None and max_value is not None:
                    q = q.filter(and_(column >= min_value, column <= max_value))
                elif min_value is not None:
                    q = q.filter(column >= min_value)
                elif max_value is not None:
                    q = q.filter(column <= max_value)
            else:  # Точное сравнение
                q = q.filter(column == value)

    # Обработка сортировки
    if sort_by and hasattr(m.Car, sort_by):
        sort_column = getattr(m.Car, sort_by)
        q = q.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    return paginate(q, params)
def get_car_cards_query(db: Session):
    return (
        db.query(m.Car)
        .options(
            selectinload(m.Car.images)
        )
        .order_by(m.Car.listing_date.desc()).all()  
    )

def create_car(db: Session, car: CarCreate, user_id: int):
    obj = m.Car(**car.dict(), user_id=user_id, uuid=uuid4())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_car(db: Session, car_id: int, car: CarUpdate):
    obj = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not obj:
        return None
    for key, value in car.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_car(db: Session, car_id: int):
    obj = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
