from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params

from database import get_db
from schemas import Review, ReviewCreate, ReviewUpdate, ReviewDetailed
import crud

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/user/{user_id}", response_model=Page[ReviewDetailed])
def get_reviews_by_user(user_id: int, params: Params = Depends(), db: Session = Depends(get_db)):
    return crud.get_reviews_by_user(db, user_id, params)

@router.post("/", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), user_id: int = 1):
    return crud.create_review(db, review, user_id)

@router.put("/{review_id}", response_model=Review)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    updated = crud.update_review(db, review_id, review)
    if not updated:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    if not crud.delete_review(db, review_id):
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
