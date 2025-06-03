from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    AdModeration,
    AdModerationUpdate,
    AdModerationWithCar,
    User
)
from crud import ad_moderation_crud
import security

router = APIRouter(prefix="/moderation", tags=["Модерация объявлений"])

@router.get("/pending", response_model=List[AdModerationWithCar], dependencies=[Depends(security.require_admin)], description="Получить список объявлений на модерации")
def get_pending_moderations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):
    return ad_moderation_crud.get_pending_moderations(db, skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=List[AdModerationWithCar], dependencies=[Depends(security.require_admin)], description="Получить список объявлений пользователя на модерации")
def get_user_moderations(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(security.require_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return ad_moderation_crud.get_user_moderations(db, user_id=user_id, skip=skip, limit=limit)

@router.get("/{car_id}", response_model=AdModerationWithCar, dependencies=[Depends(security.require_admin)], description="Получить информацию о модерации объявления по ID автомобиля")
def get_ad_moderation(
    car_id: int,
    current_user: User = Depends(security.require_user),
    db: Session = Depends(get_db)
):
    moderation = ad_moderation_crud.get_ad_moderation(db, car_id)
    if not moderation:
        raise HTTPException(status_code=404, detail="Модерация не найдена")
    
    if not current_user.is_admin and moderation.car.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    return moderation

@router.put("/{car_id}", response_model=AdModeration, dependencies=[Depends(security.require_admin)], description="Обновить информацию о модерации объявления")
def update_ad_moderation(
    car_id: int,
    moderation: AdModerationUpdate,
    current_user: User = Depends(security.require_admin),
    db: Session = Depends(get_db)
):
    db_moderation = ad_moderation_crud.get_ad_moderation(db, car_id)
    if not db_moderation:
        raise HTTPException(status_code=404, detail="Модерация не найдена")
    
    updated = ad_moderation_crud.update_ad_moderation(
        db, 
        moderation_id=db_moderation.id,
        data=moderation,
        moderator_id=current_user.id
    )
    return updated
