from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from uuid import UUID, uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import and_, asc, desc, func
from pathlib import Path

import models as m
from schemas import (
    CarCreate, CarUpdate
)

# ================ Car CRUD ================
def get_car(db: Session, car_id: int):
    return db.query(m.Car).options(selectinload(m.Car.images)).filter(m.Car.id == car_id).first()

def get_car_by_uuid(db: Session, car_uuid: UUID):
    return db.query(m.Car).options(selectinload(m.Car.images)).filter(m.Car.uuid == car_uuid).first()

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

    old_price = obj.price  # 🔥 Сохраняем старую цену

    for key, value in car.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)

    # 🔥 Если цена изменилась — добавляем запись в PriceHistory
    if 'price' in car.model_dump(exclude_unset=True) and obj.price != old_price:
        price_history = m.PriceHistory(
            car_id=obj.id,
            price=obj.price,
            change_date=datetime.now(timezone.utc)
        )
        db.add(price_history)
        db.commit()

    return obj

def delete_car(db: Session, car_id: int):
    obj = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def get_most_popular_cars(db: Session, limit: int = 10):
    subquery = (
        db.query(
            m.Favorite.car_id,
            func.count(m.Favorite.id).label("fav_count")
        )
        .group_by(m.Favorite.car_id)
        .subquery()
    )

    query = (
        db.query(m.Car)
        .join(subquery, m.Car.id == subquery.c.car_id)
        .order_by(subquery.c.fav_count.desc())
        .limit(limit)
    )

    return query.all()