from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import CarModel, CarModelCreate
import crud

router = APIRouter(prefix="/models", tags=["Models"])

@router.get("/", response_model=List[CarModel])
def get_all_models(db: Session = Depends(get_db)):
    return crud.get_models_by_brand(db, brand_id=None)  # Или сделать универсальный вывод

@router.get("/brand/{brand_id}", response_model=List[CarModel])
def get_models_by_brand(brand_id: int, db: Session = Depends(get_db)):
    return crud.get_models_by_brand(db, brand_id)

@router.get("/{model_id}", response_model=CarModel)
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.post("/", response_model=CarModel)
def create_model(model: CarModelCreate, db: Session = Depends(get_db)):
    return crud.create_model(db, model)

@router.put("/{model_id}", response_model=CarModel)
def update_model(model_id: int, model: CarModelCreate, db: Session = Depends(get_db)):
    updated = crud.update_model(db, model_id, model)
    if not updated:
        raise HTTPException(status_code=404, detail="Model not found")
    return updated

@router.delete("/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    if not crud.delete_model(db, model_id):
        raise HTTPException(status_code=404, detail="Model not found")
    return {"message": "Model deleted successfully"}