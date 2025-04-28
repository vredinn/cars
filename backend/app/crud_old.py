from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr
from sqlalchemy.orm import Session, selectinload
from passlib.context import CryptContext
from uuid import uuid4
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, Params
from sqlalchemy import asc, desc
from pathlib import Path

import models as m
from schemas import (
    CarCard, UserChangeRights, UserCreate, UserUpdate,
    BrandCreate, CarModelCreate,
    CarCreate, CarUpdate,
    ReviewCreate, ReviewUpdate,
    MessageCreate,
    FavoriteCreate,
    CarImageCreate,
    SavedSearchCreate,
    AdModerationCreate, AdModerationUpdate
)
from config import settings

UPLOAD_DIR = Path("uploads/car_images")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================ User CRUD ================
def get_user(db: Session, user_id: int):
    return db.query(m.User).filter(m.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(m.User).filter(m.User.email == email).first()

def get_users_paginated(db: Session, params: Params):
    q =db.query(m.User)
    return paginate(q, params)

def get_users(db: Session):
    return db.query(m.User).all()

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

# ================ Car CRUD ================
def get_car(db: Session, car_id: int):
    return db.query(m.Car).options(selectinload(m.Car.images)).filter(m.Car.id == car_id).first()

def get_all_cars_paginated(
    db: Session,
    filters: dict,
    sort_by: Optional[str],
    sort_order: str,
    params: Params
):
    q = db.query(m.Car)
    if filters:
        for attr, value in filters.items():
            if hasattr(m.Car, attr):
                q = q.filter(getattr(m.Car, attr) == value)
    if sort_by and hasattr(m.Car, sort_by):
        sort_column = getattr(m.Car, sort_by)
        q = q.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))
    return paginate(q, params)

def get_car_cards_query(db: Session):
    return (
        db.query(m.Car)
        .options(
            selectinload(m.Car.images)
        )
        .order_by(m.Car.listing_date.desc()).all()  
    )

def create_car(db: Session, car: CarCreate, user_id: int):
    obj = m.Car(**car.dict(), user_id=user_id, uuid=uuid4())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_car(db: Session, car_id: int, car: CarUpdate):
    obj = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not obj:
        return None
    for key, value in car.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_car(db: Session, car_id: int):
    obj = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

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

# ================ Message CRUD ================
def create_message(db: Session, msg: MessageCreate):
    obj = m.Message(**msg.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_messages(db: Session, user_id: int):
    return db.query(m.Message).filter((m.Message.sender_id == user_id) | (m.Message.receiver_id == user_id)).all()

def delete_message(db: Session, message_id: int):
    obj = db.query(m.Message).filter(m.Message.id == message_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# ================ Favorite CRUD ================
def create_favorite(db: Session, fav: FavoriteCreate):
    obj = m.Favorite(**fav.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_user_favorites(db: Session, user_id: int, params: Params):
    q = db.query(m.Favorite).filter(m.Favorite.user_id == user_id)
    return paginate(q, params)

def delete_favorite(db: Session, user_id: int, car_id: int):
    obj = db.query(m.Favorite).filter(m.Favorite.user_id == user_id, m.Favorite.car_id == car_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# ================ CarImage CRUD ================
def add_car_image(db: Session, image: CarImageCreate):
    obj = m.CarImage(**image.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_car_images(db: Session, car_id: int):
    return db.query(m.CarImage).filter(m.CarImage.car_id == car_id).all()

def delete_car_image(db: Session, image_id: int) -> bool:
    image = db.query(m.CarImage).filter(m.CarImage.id == image_id).first()
    if not image:
        return False

    # Удаляем файл
    if image.image_url:
        try:
            # Преобразуем URL в путь
            filename = image.image_url
            if filename.exists():
                filename.unlink()
        except Exception as e:
            print(f"Ошибка при удалении файла изображения: {e}")

    # Удаляем из базы
    db.delete(image)
    db.commit()
    return True

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
