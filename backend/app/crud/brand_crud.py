from sqlalchemy.orm import Session, selectinload
from sqlalchemy import asc, desc

import models as m
from schemas import (
    BrandCreate
)

# ================ Brand CRUD ================
def get_brands(db: Session):
    return db.query(m.Brand).all()

def get_brand(db: Session, brand_id: int):
    return db.query(m.Brand).filter(m.Brand.id == brand_id).first()

def create_brand(db: Session, brand: BrandCreate):
    obj = m.Brand(**brand.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_brand(db: Session, brand_id: int, brand: BrandCreate):
    obj = db.query(m.Brand).filter(m.Brand.id == brand_id).first()
    if not obj:
        return None
    for key, value in brand.dict().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_brand(db: Session, brand_id: int):
    obj = db.query(m.Brand).filter(m.Brand.id == brand_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True