from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import io

from database import get_db
from schemas import Brand, BrandCreate
import crud

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB
BRANDS_DIR = Path("brand_logos/")
CAR_IMAGE_WIDTH = 416 * 3
CAR_IMAGE_HEIGHT = 215 * 3

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

@router.post("/", response_model=Brand)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return crud.create_brand(db, brand)

@router.put("/{brand_id}", response_model=Brand)
def update_brand(brand_id: int, brand: BrandCreate, db: Session = Depends(get_db)):
    updated = crud.update_brand(db, brand_id, brand)
    if not updated:
        raise HTTPException(status_code=404, detail="Brand not found")
    return updated

@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    if not crud.delete_brand(db, brand_id):
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"message": "Brand deleted successfully"}
