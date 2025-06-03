from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from security import require_admin
from database import get_db
from schemas import CarModel, CarModelCreate
import crud

router = APIRouter(prefix="/models", tags=["Модели автомобилей"])

@router.get("/", response_model=List[CarModel], description="Получить список всех моделей автомобилей")
def get_all_models(search: str = None, db: Session = Depends(get_db)):
    return crud.get_models(db, search=search)

@router.get("/brand/{brand_id}", response_model=List[CarModel], description="Получить список моделей автомобилей по ID бренда")
def get_models_by_brand(brand_id: int, db: Session = Depends(get_db)):
    return crud.get_models_by_brand(db, brand_id)

@router.get("/{model_id}", response_model=CarModel, description="Получить информацию о модели автомобиля по ID")
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    return model

@router.post("/", response_model=CarModel, dependencies=[Depends(require_admin)], description="Создать новую модель автомобиля (только для администраторов)")
def create_model(model: CarModelCreate, db: Session = Depends(get_db)):
    return crud.create_model(db, model)

@router.put("/{model_id}", response_model=CarModel, dependencies=[Depends(require_admin)], description="Обновить информацию о модели автомобиля по ID (только для администраторов)")
def update_model(model_id: int, model: CarModelCreate, db: Session = Depends(get_db)):
    updated = crud.update_model(db, model_id, model)
    if not updated:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    return updated

@router.delete("/{model_id}", dependencies=[Depends(require_admin)], description="Удалить модель автомобиля по ID (только для администраторов)")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    if not crud.delete_model(db, model_id):
        raise HTTPException(status_code=404, detail="Модель не найдена")
    return {"message": "Модель успешно удалена"}