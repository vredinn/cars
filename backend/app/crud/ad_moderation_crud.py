from sqlalchemy.orm import Session, selectinload
from datetime import datetime

import models as m
from schemas import (
    AdModerationCreate, AdModerationUpdate
)
def get_ad_moderation(db: Session, car_id: int):
    return (
        db.query(m.AdModeration)
        .filter(m.AdModeration.car_id == car_id)
        .options(
            selectinload(m.AdModeration.car).selectinload(m.Car.images),
            selectinload(m.AdModeration.car).selectinload(m.Car.brand),
            selectinload(m.AdModeration.car).selectinload(m.Car.model),
            selectinload(m.AdModeration.car).selectinload(m.Car.user)
        )
        .first()
    )

def get_ad_moderation_by_id(db: Session, moderation_id: int):
    return db.query(m.AdModeration).filter(m.AdModeration.id == moderation_id).first()

def get_pending_moderations(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(m.AdModeration)
        .options(
            selectinload(m.AdModeration.car).selectinload(m.Car.images),
            selectinload(m.AdModeration.car).selectinload(m.Car.brand),
            selectinload(m.AdModeration.car).selectinload(m.Car.model),
            selectinload(m.AdModeration.car).selectinload(m.Car.user)
        )
        .filter(m.AdModeration.status == m.AdModerationStatusEnum.pending)
        .order_by(m.AdModeration.moderation_date.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_user_moderations(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(m.AdModeration)
        .join(m.Car)
        .options(
            selectinload(m.AdModeration.car).selectinload(m.Car.images),
            selectinload(m.AdModeration.car).selectinload(m.Car.brand),
            selectinload(m.AdModeration.car).selectinload(m.Car.model),
            selectinload(m.AdModeration.car).selectinload(m.Car.user)
        )
        .filter(m.Car.user_id == user_id)
        .order_by(m.AdModeration.moderation_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_ad_moderation(db: Session, entry: AdModerationCreate):
    obj = m.AdModeration(**entry.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_ad_moderation(db: Session, moderation_id: int, data: AdModerationUpdate, moderator_id: int = None):
    obj = db.query(m.AdModeration).filter(m.AdModeration.id == moderation_id).first()
    if not obj:
        return None
    
    update_data = data.dict(exclude_unset=True)
    if moderator_id:
        update_data["moderator_id"] = moderator_id
        update_data["moderation_date"] = datetime.now()
    
    for key, value in update_data.items():
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
