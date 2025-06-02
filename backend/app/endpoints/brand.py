from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List
from PIL import Image
from pathlib import Path
import io
from uuid import uuid4
from security import require_admin
from database import get_db
from schemas import Brand, BrandCreate
import crud

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB

# ✅ относительный путь
BRANDS_DIR = Path("brand_logos")
BRANDS_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/", response_model=List[Brand])
def get_brands(db: Session = Depends(get_db)):
    return crud.get_brands(db)


@router.get("/{brand_id}", response_model=Brand)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = crud.get_brand(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.post("/", response_model=Brand, dependencies=[Depends(require_admin)])
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return crud.create_brand(db, brand)


@router.post("/upload", response_model=str, dependencies=[Depends(require_admin)])
async def upload_brand_logo(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Допустимы только JPEG и PNG")

    file.file.seek(0, io.SEEK_END)
    if file.file.tell() > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Слишком большой файл")
    file.file.seek(0)

    try:
        image = Image.open(file.file).convert("RGBA")
        
        # Определяем минимальную сторону изображения
        width, height = image.size
        min_side = min(width, height)
        
        # Координаты для кропа (центрированный квадрат)
        left = (width - min_side) // 2
        top = (height - min_side) // 2
        right = (width + min_side) // 2
        bottom = (height + min_side) // 2
        
        # Выполняем кроп
        image = image.crop((left, top, right, bottom))
        
        # Ресайз до нужного размера (если требуется)
        image = image.resize((512, 512), Image.LANCZOS)
        
        filename = f"{uuid4().hex}.png"
        save_path = BRANDS_DIR / filename
        image.save(save_path, "PNG", quality=95)  # Увеличил качество
        
        return f"/brand_logos/{filename}"
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Ошибка обработки изображения: {str(e)}"
        )


@router.delete("/image/{filename}", dependencies=[Depends(require_admin)])
def delete_brand_image(filename: str):
    try:
        filepath = BRANDS_DIR / Path(filename).name
        if filepath.exists():
            filepath.unlink()
            return {"message": "Изображение удалено"}
        else:
            raise HTTPException(status_code=404, detail="Файл не найден")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка удаления изображения: {e}")


@router.put("/{brand_id}", response_model=Brand, dependencies=[Depends(require_admin)])
def update_brand(brand_id: int, brand: BrandCreate, db: Session = Depends(get_db)):

    updated = crud.update_brand(db, brand_id, brand)
    if not updated:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated


@router.delete("/{brand_id}", dependencies=[Depends(require_admin)])
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    if not crud.delete_brand(db, brand_id):
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"message": "Brand deleted successfully"}
