from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params

from database import get_db
from schemas import Favorite, FavoriteCreate
import crud

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/user_paginated/{user_uuid}", response_model=Page[Favorite])
def get_user_favorites(user_uuid: UUID, params: Params = Depends(), db: Session = Depends(get_db)):
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    return crud.get_user_favorites_paginated(db, user_id, params=params)

@router.get("/user/{user_uuid}", response_model=List[Favorite])
def get_user_favorites(user_uuid: UUID, db: Session = Depends(get_db)):
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    return crud.get_user_favorites(db, user_id)

@router.get("/check/{user_uuid}/{car_uuid}")
def check_favorite(user_uuid: UUID, car_uuid: UUID, db: Session = Depends(get_db)):
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    car_id = crud.get_car_id_by_uuid(db, car_uuid)

    if crud.check_favorite(db, user_id, car_id):
        return True
    else:
        return False

@router.post("/", response_model=Favorite)
def create_favorite(data: FavoriteCreate, db: Session = Depends(get_db)):
    user_id = crud.get_user_id_by_uuid(db, data.user_uuid)
    car_id = crud.get_car_id_by_uuid(db, data.car_uuid)

    return crud.create_favorite(db, user_id, car_id)

@router.delete("/{user_uuid}/{car_uuid}")
def delete_favorite(user_uuid: UUID, car_uuid: UUID, db: Session = Depends(get_db)):
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    car_id = crud.get_car_id_by_uuid(db, car_uuid)
    if not crud.delete_favorite(db, user_id, car_id):
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite deleted successfully"}