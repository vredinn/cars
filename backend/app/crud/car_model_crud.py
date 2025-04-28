from typing import Optional
from sqlalchemy.orm import Session, selectinload
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import asc, desc

import models as m
from schemas import CarModelCreate

# ================ CarModel CRUD ================
def get_model(db: Session, model_id: int):
    return db.query(m.CarModel).filter(m.CarModel.id == model_id).first()

def get_models_by_brand(db: Session, brand_id: Optional[int]):
    q = db.query(m.CarModel)
    if brand_id:
        q = q.filter(m.CarModel.brand_id == brand_id)
    return q.all()

def create_model(db: Session, model: CarModelCreate):
    obj = m.CarModel(**model.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_model(db: Session, model_id: int, model: CarModelCreate):
    obj = db.query(m.CarModel).filter(m.CarModel.id == model_id).first()
    if not obj:
        return None
    for key, value in model.dict().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_model(db: Session, model_id: int):
    obj = db.query(m.CarModel).filter(m.CarModel.id == model_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True