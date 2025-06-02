from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from uuid import UUID, uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import and_, asc, desc, func, literal_column, or_
from pathlib import Path

import models as m
from schemas import (
    CarCreate, CarUpdate, AdModerationCreate
)

# ================ Car CRUD ================
def get_car_id_by_uuid(db: Session, car_uuid: UUID):
    return db.query(m.Car).filter(m.Car.uuid == car_uuid).first().id

def get_car_uuid_by_id(db: Session, car_id: int):
    return db.query(m.Car).filter(m.Car.id == car_id).first().uuid

def get_car(db: Session, car_id: int):
    return (
        db.query(m.Car)
        .options(
            selectinload(m.Car.images),
            selectinload(m.Car.moderation),
            selectinload(m.Car.brand),
            selectinload(m.Car.model),
            selectinload(m.Car.user),
            selectinload(m.Car.price_history)
        )
        .filter(m.Car.id == car_id)
        .first()
    )

def get_car_by_uuid(db: Session, car_uuid: UUID):
    return (
        db.query(m.Car)
        .options(
            selectinload(m.Car.images),
            selectinload(m.Car.moderation),
            selectinload(m.Car.brand),
            selectinload(m.Car.model),
            selectinload(m.Car.user),
            selectinload(m.Car.price_history)
        )
        .filter(m.Car.uuid == car_uuid)
        .first()
    )

def check_ownership(db: Session, car_uuid: UUID, user_uuid: UUID):
    return db.query(m.Car).filter(and_(m.Car.uuid == car_uuid, m.Car.user.has(uuid=user_uuid))).first() is not None

def get_all_cars_paginated(
    db: Session,
    filters: dict,
    sort_by: Optional[str],
    sort_order: str,
    params: Params,
    user_id: Optional[int] = None
):
    q = db.query(m.Car).options(
        selectinload(m.Car.moderation),
        selectinload(m.Car.brand),
        selectinload(m.Car.model)
    )

    # Фильтр по модерации: показываем только одобренные объявления
    # или все объявления владельца, если указан user_id
    if user_id:
        q = q.filter(
            or_(
                m.Car.user_id == user_id,
                m.Car.moderation.has(status=m.AdModerationStatusEnum.approved)
            )
        )
    else:
        q = q.filter(m.Car.moderation.has(status=m.AdModerationStatusEnum.approved))

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
    params: Params,
    show_only_approved: bool = False
):
    q = (
        db.query(m.Car)
        .options(
            selectinload(m.Car.images),
            selectinload(m.Car.moderation),
            selectinload(m.Car.brand),
            selectinload(m.Car.model),
            selectinload(m.Car.user),
            selectinload(m.Car.price_history)
        )
        .filter(m.Car.user.has(uuid=user_uuid))
    )

    if show_only_approved:
        q = q.join(m.AdModeration).filter(m.AdModeration.status == "Одобрено")

    return paginate(q, params)


def create_car(db: Session, car: CarCreate, user_id: int):
    # Создаем объявление
    obj = m.Car(**car.dict(), uuid=uuid4(), user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # Создаем запись о модерации
    moderation = m.AdModeration(
        car_id=obj.id,
        status=m.AdModerationStatusEnum.pending
    )
    db.add(moderation)
    db.commit()

    return obj

def update_car(db: Session, car_id: int, car: CarUpdate):
    obj = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not obj:
        return None

    old_price = obj.price

    for key, value in car.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    # При обновлении объявления сбрасываем статус модерации на "На проверке"
    moderation = db.query(m.AdModeration).filter(m.AdModeration.car_id == car_id).first()
    if moderation:
        moderation.status = m.AdModerationStatusEnum.pending
        moderation.moderator_comment = None
        moderation.moderator_id = None
        moderation.moderation_date = datetime.now(timezone.utc)

    db.commit()
    db.refresh(obj)

    # Если цена изменилась — добавляем запись в PriceHistory
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

def get_most_popular_cars(db: Session, limit: int = 10, user_id: Optional[int] = None):
    subquery = (
        db.query(
            m.Favorite.car_id,
            func.count(m.Favorite.id).label("fav_count")
        )
        .group_by(m.Favorite.car_id)
        .subquery()
    )

    q = (
        db.query(m.Car)
        .join(subquery, m.Car.id == subquery.c.car_id)
        .filter(m.Car.is_sold == False)
    )

    # Фильтр по модерации
    if user_id:
        q = q.filter(
            or_(
                m.Car.user_id == user_id,
                m.Car.moderation.has(status=m.AdModerationStatusEnum.approved)
            )
        )
    else:
        q = q.filter(m.Car.moderation.has(status=m.AdModerationStatusEnum.approved))

    return q.order_by(subquery.c.fav_count.desc()).limit(limit).all()

def get_cars_paginated(
    db: Session,
    params: Params,
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
    center_latitude: Optional[float] = None,
    center_longitude: Optional[float] = None,
    radius_km: Optional[float] = None,
    color: Optional[str] = None,
    drive_type: Optional[str] = None,
    transmission: Optional[str] = None,
    fuel_type: Optional[str] = None,
    steering_side: Optional[str] = None,
    car_condition: Optional[str] = None,
    is_sold: Optional[bool] = False,
    body_type: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc",
    show_only_approved: bool = False
):
    query = db.query(m.Car).options(
        selectinload(m.Car.images),
        selectinload(m.Car.moderation),
        selectinload(m.Car.brand),
        selectinload(m.Car.model),
        selectinload(m.Car.user),
        selectinload(m.Car.price_history)
    )

    # Применяем фильтры
    if brand_id:
        query = query.filter(m.Car.brand_id == brand_id)
    if model_id:
        query = query.filter(m.Car.model_id == model_id)
    if min_price:
        query = query.filter(m.Car.price >= min_price)
    if max_price:
        query = query.filter(m.Car.price <= max_price)
    if min_year:
        query = query.filter(m.Car.year >= min_year)
    if max_year:
        query = query.filter(m.Car.year <= max_year)
    if min_mileage:
        query = query.filter(m.Car.mileage >= min_mileage)
    if max_mileage:
        query = query.filter(m.Car.mileage <= max_mileage)
    if min_engine_capacity:
        query = query.filter(m.Car.engine_capacity >= min_engine_capacity)
    if max_engine_capacity:
        query = query.filter(m.Car.engine_capacity <= max_engine_capacity)
    if min_engine_power:
        query = query.filter(m.Car.engine_power >= min_engine_power)
    if max_engine_power:
        query = query.filter(m.Car.engine_power <= max_engine_power)
    if min_latitude:
        query = query.filter(m.Car.latitude >= min_latitude)
    if max_latitude:
        query = query.filter(m.Car.latitude <= max_latitude)
    if min_longitude:
        query = query.filter(m.Car.longitude >= min_longitude)
    if max_longitude:
        query = query.filter(m.Car.longitude <= max_longitude)
    if color:
        query = query.filter(m.Car.color == color)
    if drive_type:
        query = query.filter(m.Car.drive_type == drive_type)
    if transmission:
        query = query.filter(m.Car.transmission == transmission)
    if fuel_type:
        query = query.filter(m.Car.fuel_type == fuel_type)
    if steering_side:
        query = query.filter(m.Car.steering_side == steering_side)
    if car_condition:
        query = query.filter(m.Car.car_condition == car_condition)
    if is_sold is False:
        query = query.filter(m.Car.is_sold == False)
    if body_type:
        query = query.filter(m.Car.body_type == body_type)

    # Фильтр по радиусу
    if center_latitude and center_longitude and radius_km:
        # Используем формулу гаверсинусов для расчета расстояния
        earth_radius = 6371  # радиус Земли в километрах
        query = query.filter(
            func.acos(
                func.sin(func.radians(center_latitude)) * func.sin(func.radians(m.Car.latitude)) +
                func.cos(func.radians(center_latitude)) * func.cos(func.radians(m.Car.latitude)) *
                func.cos(func.radians(m.Car.longitude) - func.radians(center_longitude))
            ) * earth_radius <= radius_km
        )

    # Фильтр по статусу модерации
    if show_only_approved:
        query = query.join(m.AdModeration).filter(m.AdModeration.status == "Одобрено")

    # Сортировка
    if sort_by:
        if sort_by == "price":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(m.Car.price))
        elif sort_by == "year":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(m.Car.year))
        elif sort_by == "mileage":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(m.Car.mileage))
        elif sort_by == "listing_date":
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(m.Car.listing_date))
    else:
        # По умолчанию сортируем по дате добавления
        query = query.order_by(desc(m.Car.listing_date))

    return paginate(query, params)