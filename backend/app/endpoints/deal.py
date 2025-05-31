from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database import get_db
from security import require_user
from schemas import Deal, DealCreate
from crud import deal_crud
from models import User, Deal as DealModel, Car

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.post("/create", response_model=Deal)
def create_deal(
    deal_create: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    # Check if user is the seller
    car = db.query(Car).filter(Car.uuid == deal_create.car_uuid).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    if car.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only seller can create a deal"
        )
    
    if car.is_sold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car is already sold"
        )
    
    deal = deal_crud.create_deal(db, deal_create, current_user.id)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create deal"
        )
    return deal

@router.post("/{deal_uuid}/cancel")
def cancel_deal(
    deal_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    success = deal_crud.cancel_deal(db, deal_uuid, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not cancel deal"
        )
    return {"message": "Deal cancelled successfully"}

@router.get("/car/{car_uuid}", response_model=Deal)
def get_car_deal(
    car_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    deal = deal_crud.get_car_deal(db, car_uuid)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    return deal

@router.get("/{deal_uuid}", response_model=Deal)
def get_deal(
    deal_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    deal = deal_crud.get_deal_by_uuid(db, deal_uuid)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deal not found"
        )
    return deal

@router.get("/user/deals", response_model=List[Deal])
def get_user_deals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    return deal_crud.get_user_deals(db, current_user.id, skip, limit) 