import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from PIL import Image
from PIL import ImageOps
from pathlib import Path
from database import get_db
from schemas import CarImage, CarImageCreate
import models as m
import crud
import io


ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB
UPLOAD_DIR = Path("uploads/car_images")
CAR_IMAGE_WIDTH = 416 * 3
CAR_IMAGE_HEIGHT = 215 * 3

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter(prefix="/car-images", tags=["Car Images"])


@router.get("/car/{car_id}", response_model=list[CarImage])
def get_images_by_car(car_id: int, db: Session = Depends(get_db)):
    return crud.get_car_images(db, car_id)

@router.post("/", response_model=CarImageCreate)
async def create_car_image(
    car_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Получаем машину
    car = db.query(m.Car).filter(m.Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # 2. Проверяем тип и размер
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Допустимы только JPEG и PNG")

    file.file.seek(0, io.SEEK_END)
    if file.file.tell() > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Слишком большой файл")
    file.file.seek(0)

    try:
        image = Image.open(file.file).convert("RGB")
        # image = ImageOps.fit(image, (CAR_IMAGE_WIDTH, CAR_IMAGE_HEIGHT), Image.LANCZOS, centering=(0.5, 0.5))

        # 3. Путь: uploads/car_images/<uuid>/xxx.webp
        car_dir = UPLOAD_DIR / str(car.uuid)
        car_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.webp"
        save_path = car_dir / filename
        image.save(save_path, "webp", quality=80)

    except Exception:
        raise HTTPException(status_code=400, detail="Ошибка обработки изображения")

    image_url = f"/uploads/car_images/{car.uuid}/{filename}"
    new_image = crud.add_car_image(db, CarImageCreate(car_id=car_id, image_url=image_url))
    return new_image

@router.delete("/{image_id}")
def delete_car_image(image_id: int, db: Session = Depends(get_db)):
    if not crud.delete_car_image(db, image_id):
        raise HTTPException(status_code=404, detail="Car image not found")
    return {"message": "Car image deleted successfully"}
