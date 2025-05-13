
from pydantic import EmailStr
from sqlalchemy.orm import Session, selectinload
from passlib.context import CryptContext
from uuid import UUID, uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import asc, desc
from pathlib import Path

import models as m
from schemas import (
    UserChangeRights, UserCreate, UserUpdate
)
from config import settings

UPLOAD_DIR = Path("uploads/car_images")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================ User CRUD ================
def get_user(db: Session, user_id: int):
    return db.query(m.User).filter(m.User.id == user_id).first()

def get_user_by_uuid(db: Session, user_uuid: UUID):
    return db.query(m.User).filter(m.User.uuid == user_uuid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(m.User).filter(m.User.email == email).first()

def get_users(db: Session):
    return db.query(m.User).all()

def get_popular_users(db: Session):
    return db.query(m.User).filter(m.User.is_admin == False).order_by(desc(m.User.rating)).limit(4).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password + settings.SALT)
    db_user = m.User(uuid=uuid4(), name=user.name, email=user.email, phone=user.phone, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(m.User).filter(m.User.id == user_id).first()
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"] + settings.SALT)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def user_change_rights(db: Session, user_id: int, user_update: UserChangeRights):    
    db_user = db.query(m.User).filter(m.User.id == user_id).first()
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(m.User).filter(m.User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, email: EmailStr, password: str):
    user = get_user_by_email(db, email)
    if user and pwd_context.verify(password + settings.SALT, user.password):
        return user
    return None

