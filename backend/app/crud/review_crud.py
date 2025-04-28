from sqlalchemy.orm import Session, selectinload
from uuid import uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params

import models as m
from schemas import (
    ReviewCreate, ReviewUpdate
)


# ================ Review CRUD ================
def get_reviews_by_user(db: Session, user_id: int, params: Params):
    q = db.query(m.Review).filter(m.Review.user_id == user_id)
    return paginate(q, params)

def create_review(db: Session, review: ReviewCreate, user_id: int):
    obj = m.Review(**review.dict(), user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_review(db: Session, review_id: int, data: ReviewUpdate):
    obj = db.query(m.Review).filter(m.Review.id == review_id).first()
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_review(db: Session, review_id: int):
    obj = db.query(m.Review).filter(m.Review.id == review_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True