from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from uuid import UUID, uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import and_, asc, desc, func, literal_column
from pathlib import Path

import models as m
from schemas import (
    CarCreate, CarUpdate
)

# ================ Car CRUD ================
def get_car_id_by_uuid(db: Session, car_uuid: UUID):
    return db.query(m.Car).filter(m.Car.uuid == car_uuid).first().id

def get_car_uuid_by_id(db: Session, car_id: int):
    return db.query(m.Car).filter(m.Car.id == car_id).first().uuid

def get_car(db: Session, car_id: int):
    return db.query(m.Car).options(selectinload(m.Car.images)).filter(m.Car.id == car_id).first()

def get_car_by_uuid(db: Session, car_uuid: UUID):
    return db.query(m.Car).options(selectinload(m.Car.images)).filter(m.Car.uuid == car_uuid).first()

def check_ownership(db: Session, car_uuid: UUID, user_uuid: UUID):
    return db.query(m.Car).filter(and_(m.Car.uuid == car_uuid, m.Car.user.has(uuid=user_uuid))).first() is not None



def get_all_cars_paginated(
    db: Session,
    filters: dict,
    sort_by: Optional[str],
    sort_order: str,
    params: Params
):
    q = db.query(m.Car)

    lat_center = filters.pop("center_latitude", None)
    lon_center = filters.pop("center_longitude", None)
    radius_km = filters.pop("radius_km", None)

    if lat_center is not None and lon_center is not None and radius_km is not None:
        distance_expr = 6371 * func.acos(
            func.cos(func.radians(lat_center)) *
            func.cos(func.radians(m.Car.latitude)) *
            func.cos(func.radians(m.Car.longitude) - func.radians(lon_center)) +
            func.sin(func.radians(lat_center)) *
            func.sin(func.radians(m.Car.latitude))
        )
        q = q.filter(distance_expr <= radius_km)

    for attr, value in filters.items():
        if hasattr(m.Car, attr):
            column = getattr(m.Car, attr)
            if isinstance(value, tuple) and len(value) == 2:
                min_value, max_value = value
                if min_value is not None and max_value is not None:
                    q = q.filter(and_(column >= min_value, column <= max_value))
                elif min_value is not None:
                    q = q.filter(column >= min_value)
                elif max_value is not None:
                    q = q.filter(column <= max_value)
            else:
                q = q.filter(column == value)

    if sort_by and hasattr(m.Car, sort_by):
        sort_column = getattr(m.Car, sort_by)
        q = q.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    return paginate(q, params)

def get_user_cars_paginated(
    db: Session,
    user_uuid: UUID,
    params: Params
):
    q = db.query(m.Car).filter(m.Car.user.has(uuid=user_uuid))
    # q = db.query(m.Car)
    return paginate(q, params)


def get_car_cards_query(db: Session):
    return (
        db.query(m.Car)
        .options(
            selectinload(m.Car.images)
        )
        .order_by(m.Car.listing_date.desc()).all()  
    )

def create_car(db: Session, car: CarCreate, user_id: UUID):
    obj = m.Car(**car.dict(), uuid=uuid4(), user_id=user_id)
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