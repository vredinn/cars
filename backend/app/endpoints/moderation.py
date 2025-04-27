from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import AdModeration, AdModerationCreate, AdModerationUpdate
import crud

router = APIRouter(prefix="/moderation", tags=["Moderation"])

@router.get("/{car_id}", response_model=AdModeration)
def get_ad_moderation(car_id: int, db: Session = Depends(get_db)):
    moderation = crud.get_ad_moderation(db, car_id)
    if not moderation:
        raise HTTPException(status_code=404, detail="Moderation entry not found")
    return moderation

@router.post("/", response_model=AdModeration)
def create_ad_moderation(entry: AdModerationCreate, db: Session = Depends(get_db)):
    return crud.create_ad_moderation(db, entry)

@router.put("/{moderation_id}", response_model=AdModeration)
def update_ad_moderation(moderation_id: int, entry: AdModerationUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ad_moderation(db, moderation_id, entry)
    if not updated:
        raise HTTPException(status_code=404, detail="Moderation entry not found")
    return updated

@router.delete("/{moderation_id}")
def delete_ad_moderation(moderation_id: int, db: Session = Depends(get_db)):
    # (Если нужно реализовать удаление модерации)
    moderation = crud.get_ad_moderation(db, moderation_id)
    if not moderation:
        raise HTTPException(status_code=404, detail="Moderation entry not found")
    db.delete(moderation)
    db.commit()
    return {"message": "Moderation entry deleted successfully"}
