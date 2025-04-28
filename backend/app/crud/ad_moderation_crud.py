from sqlalchemy.orm import Session, selectinload
from uuid import uuid4
from sqlalchemy import asc, desc

import models as m
from schemas import (
    AdModerationCreate, AdModerationUpdate
)
# ================ AdModeration CRUD ================
def get_ad_moderation(db: Session, car_id: int):
    return db.query(m.AdModeration).filter(m.AdModeration.car_id == car_id).first()

def create_ad_moderation(db: Session, entry: AdModerationCreate):
    obj = m.AdModeration(**entry.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_ad_moderation(db: Session, moderation_id: int, data: AdModerationUpdate):
    obj = db.query(m.AdModeration).filter(m.AdModeration.id == moderation_id).first()
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_ad_moderation(db: Session, moderation_id: int):
    obj = db.query(m.AdModeration).filter(m.AdModeration.id == moderation_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
