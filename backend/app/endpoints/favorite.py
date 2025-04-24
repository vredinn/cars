from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params

from database import get_db
from schemas import Favorite, FavoriteCreate
import crud

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/user/{user_id}", response_model=Page[Favorite])
def get_user_favorites(user_id: int, params: Params = Depends(), db: Session = Depends(get_db)):
    return crud.get_user_favorites(db, user_id, params=params)

@router.post("/", response_model=Favorite)
def create_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    return crud.create_favorite(db, favorite)

@router.delete("/{user_id}/{car_id}")
def delete_favorite(user_id: int, car_id: int, db: Session = Depends(get_db)):
    if not crud.delete_favorite(db, user_id, car_id):
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite deleted successfully"}