from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from database import get_db
from schemas import *
import crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.get("/", response_model=List[UserBase])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/{user_uuid}", response_model=User)
def read_user_by_uuid(user_uuid: UUID, db: Session = Depends(get_db)):
    user = crud.get_user_by_uuid(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_uuid}/cars", response_model=List[CarCard])
def read_user_cars(user_uuid: UUID, db: Session = Depends(get_db)):
    user = crud.get_user_by_uuid(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")    
    cars = user.cars
    if not cars:
        raise HTTPException(status_code=404, detail="Cars not found")
    return cars

@router.get("_popular", response_model=List[User])
def read_popular_users(db: Session = Depends(get_db)):
    return crud.get_popular_users(db)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.put("/change_rights/{user_id}", response_model=User)
def update_user(user_id: int, user: UserChangeRights, db: Session = Depends(get_db)):
    updated = crud.user_change_rights(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}