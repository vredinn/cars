from sqlalchemy.orm import Session, selectinload
from passlib.context import CryptContext
from uuid import uuid4
from sqlalchemy import asc, desc
from pathlib import Path
from uuid import UUID
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

def get_car_images(db: Session, car_uuid: UUID):
    return db.query(m.CarImage).filter(m.CarImage.car_uuid == car_uuid).all()

def is_car_image_owner(db: Session, image_id: int, user_id: int) -> bool:
    image = db.query(m.CarImage).filter(m.CarImage.id == image_id).first()
    return image and image.car.user_id == user_id

def delete_car_image(db: Session, image_id: int) -> bool:
    image = db.query(m.CarImage).filter(m.CarImage.id == image_id).first()
    if not image:
        return False

    # Удаляем файл
    if image.image_url:
        try:
            # Предполагаем, что image_url содержит относительный путь, например, "uploads/image.jpg"
            base_dir = Path(__file__).resolve().parent.parent / "static"
            file_path = base_dir / image.image_url
            if file_path.exists():
                file_path.unlink()
            else:
                print(f"Файл не найден: {file_path}")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

    # Удаляем из базы
    db.delete(image)
    db.commit()
    return True
