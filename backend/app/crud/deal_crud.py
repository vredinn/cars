from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from uuid import UUID

from models import Deal, Car, User
from schemas import DealCreate

def get_deal(db: Session, car_uuid: UUID) -> Optional[Deal]:
    car = db.query(Car).filter(Car.uuid == car_uuid).first()
    if not car:
        return None
    
    return db.query(Deal).filter(Deal.car_id == car.id).first()

def create_deal(db: Session, deal_create: DealCreate, seller_id: int) -> Optional[Deal]:
    car = db.query(Car).filter(Car.uuid == deal_create.car_uuid).first()
    if not car or car.user_id != seller_id or car.is_sold:
        return None

    buyer = db.query(User).filter(User.uuid == deal_create.buyer_uuid).first()
    if not buyer or buyer.id == seller_id:
        return None

    db_deal = Deal(
        car_id=car.id,
        seller_id=seller_id,
        buyer_id=buyer.id
    )
    
    car.is_sold = True
    
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    return db_deal

def get_user_deals(db: Session, user_id: int) -> List[Deal]:
    return (
        db.query(Deal)
        .filter(or_(Deal.seller_id == user_id, Deal.buyer_id == user_id))
        .order_by(Deal.created_at.desc())
        .all()
    )

def get_deal_by_uuid(db: Session, deal_uuid: UUID) -> Optional[Deal]:
    return db.query(Deal).filter(Deal.uuid == deal_uuid).first()

def get_car_deal(db: Session, car_uuid: UUID) -> Optional[Deal]:
    car = db.query(Car).filter(Car.uuid == car_uuid).first()
    if not car:
        return None
    
    return db.query(Deal).filter(Deal.car_id == car.id).first() 