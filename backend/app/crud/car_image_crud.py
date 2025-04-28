from sqlalchemy.orm import Session, selectinload
from passlib.context import CryptContext
from uuid import uuid4
from sqlalchemy import asc, desc
from pathlib import Path

import models as m
from schemas import CarImageCreate
from config import settings

UPLOAD_DIR = Path("uploads/car_images")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
