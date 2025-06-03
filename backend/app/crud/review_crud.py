from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID

import models as m
from schemas import ReviewCreate, ReviewUpdate

def get_reviews_by_seller(db: Session, seller_uuid: UUID):
    return (
        db.query(m.Review, m.User)
        .join(m.User, m.User.uuid == m.Review.user_uuid)
        .filter(m.Review.seller_uuid == seller_uuid)
        .order_by(m.Review.review_date.desc())
        .all()
    )

def _recalculate_seller_rating(db: Session, seller_uuid: UUID):
    """Helper function to recalculate seller's rating"""
    avg_rating = db.query(func.avg(m.Review.rating)).filter(m.Review.seller_uuid == seller_uuid).scalar() or 0
    seller = db.query(m.User).filter(m.User.uuid == seller_uuid).first()
    if seller:
        seller.rating = float(avg_rating)
        db.commit()

def create_review(db: Session, review_create: ReviewCreate, user_uuid: UUID) -> Optional[m.Review]:
    deal = db.query(m.Deal).filter(m.Deal.uuid == review_create.deal_uuid).first()
    if not deal:
        return None
    
    if deal.buyer_uuid != user_uuid:
        return None

    existing_review = db.query(m.Review).filter(m.Review.deal_uuid == deal.uuid).first()
    if existing_review:
        return None

    db_review = m.Review(
        user_uuid=user_uuid,
        seller_uuid=deal.seller_uuid,
        deal_uuid=deal.uuid,
        review_text=review_create.review_text,
        rating=review_create.rating
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    _recalculate_seller_rating(db, deal.seller_uuid)
    
    return db_review

def update_review(db: Session, review_uuid: UUID, data: ReviewUpdate):
    obj = db.query(m.Review).filter(m.Review.uuid == review_uuid).first()
    if not obj:
        return None
        
    seller_uuid = obj.seller_uuid
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    
    _recalculate_seller_rating(db, seller_uuid)
    
    return obj

def delete_review(db: Session, review_uuid: UUID):
    obj = db.query(m.Review).filter(m.Review.uuid == review_uuid).first()
    if not obj:
        return False
        
    seller_uuid = obj.seller_uuid
    
    db.delete(obj)
    db.commit()
    
    _recalculate_seller_rating(db, seller_uuid)
    
    return True

def get_reviews_for_seller(db: Session, seller_uuid: UUID, skip: int = 0, limit: int = 10) -> List[m.Review]:
    """Get all reviews for a seller"""
    return (
        db.query(m.Review)
        .filter(m.Review.seller_uuid == seller_uuid)
        .order_by(m.Review.review_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_deal_review(db: Session, deal_uuid: UUID) -> Optional[m.Review]:
    """Get review for a specific deal"""
    return db.query(m.Review).filter(m.Review.deal_uuid == deal_uuid).first()

def get_reviews_by_seller_paginated(db: Session, seller_uuid: UUID, params: Params):
    """Get paginated reviews for a seller"""
    query = (
        db.query(m.Review)
        .filter(m.Review.seller_uuid == seller_uuid)
        .order_by(m.Review.review_date.desc())
    )
    return paginate(query, params)