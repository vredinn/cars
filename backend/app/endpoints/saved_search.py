from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import SavedSearch, SavedSearchCreate
import crud

router = APIRouter(prefix="/saved-searches", tags=["Saved Searches"])

@router.get("/user/{user_id}", response_model=list[SavedSearch])
def get_saved_searches(user_id: int, db: Session = Depends(get_db)):
    return crud.get_saved_searches(db, user_id)

@router.post("/", response_model=SavedSearch)
def create_saved_search(search: SavedSearchCreate, db: Session = Depends(get_db)):
    return crud.create_saved_search(db, search)

@router.delete("/{search_id}")
def delete_saved_search(search_id: int, db: Session = Depends(get_db)):
    if not crud.delete_saved_search(db, search_id):
        raise HTTPException(status_code=404, detail="Saved search not found")
    return {"message": "Saved search deleted successfully"}