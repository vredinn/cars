from sqlalchemy.orm import Session, selectinload
from uuid import uuid4, UUID
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import  Params

import models as m
from schemas import (
    FavoriteCreate
)
# ================ Favorite CRUD ================
def create_favorite(db: Session, user_id : int, car_id: int):
    obj = m.Favorite(car_id = car_id, user_id = user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_user_favorites_paginated(db: Session, user_id: int, params: Params):
    q = db.query(m.Favorite).filter(m.Favorite.user_id == user_id)
    return paginate(q, params)

def get_user_favorites(db: Session, user_id: int):
    return db.query(m.Favorite).filter(m.Favorite.user_id == user_id).all()

def delete_favorite(db: Session, user_id: int, car_id: int):
    obj = db.query(m.Favorite).filter(m.Favorite.user_id == user_id, m.Favorite.car_id == car_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def check_favorite(db: Session, user_id: int, car_id: int):
    return bool(db.query(m.Favorite).filter(m.Favorite.user_id == user_id, m.Favorite.car_id == car_id).first())
