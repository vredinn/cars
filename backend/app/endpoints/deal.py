from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database import get_db
from security import require_user
from schemas import Deal, DealCreate
from crud import deal_crud
from models import User, Car

router = APIRouter(prefix="/deals", tags=["Сделки"])

@router.post("/create", response_model=Deal, description="Создать сделку")
def create_deal(
    deal_create: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    car = db.query(Car).filter(Car.uuid == deal_create.car_uuid).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Машина не найдена"
        )
    
    if car.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только владелец машины может создать сделку"
        )
    
    if car.is_sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Машина уже продана"
        )
    
    deal = deal_crud.create_deal(db, deal_create, current_user.id)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось создать сделку"
        )
    return deal

@router.get("/car/{car_uuid}", response_model=Deal, description="Получить сделку по машине")
def get_car_deal(
    car_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    deal = deal_crud.get_car_deal(db, car_uuid)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сделка не найдена"
        )
    return deal

@router.get("/{deal_uuid}", response_model=Deal, description="Получить сделку по UUID")
def get_deal(
    deal_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    deal = deal_crud.get_deal_by_uuid(db, deal_uuid)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сделка не найдена"
        )
    return deal

@router.get("/user/deals", response_model=List[Deal], description="Получить список сделок пользователя")
def get_user_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    return deal_crud.get_user_deals(db, current_user.id) 