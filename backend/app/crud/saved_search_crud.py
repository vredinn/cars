from sqlalchemy.orm import Session, selectinload
from uuid import uuid4
from sqlalchemy import asc, desc

import models as m
from schemas import (
    SavedSearchCreate
)
# ================ SavedSearch CRUD ================
def get_saved_searches(db: Session, user_id: int):
    return db.query(m.SavedSearch).filter(m.SavedSearch.user_id == user_id).all()

def create_saved_search(db: Session, data: SavedSearchCreate):
    obj = m.SavedSearch(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_saved_search(db: Session, search_id: int):
    obj = db.query(m.SavedSearch).filter(m.SavedSearch.id == search_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True