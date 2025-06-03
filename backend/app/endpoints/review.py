from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params, paginate
from typing import List
from uuid import UUID
import logging
from sqlalchemy.sql import func

from database import get_db
from schemas import Review, ReviewCreate, ReviewUpdate, ReviewResponse
from crud import review_crud
from security import require_user
from models import User, Review as ReviewModel

router = APIRouter(prefix="/reviews", tags=["Отзывы"])

@router.get("/seller/{seller_uuid}", response_model=List[ReviewResponse], description="Получить все отзывы продавца")
def get_seller_reviews(
    seller_uuid: UUID,
    db: Session = Depends(get_db)
):
    try:
        seller = db.query(User).filter(User.uuid == seller_uuid).first()
        if not seller:
            raise HTTPException(status_code=404, detail="Seller not found")
        
        reviews = review_crud.get_reviews_by_seller(db, seller_uuid)
        
        review_responses = []
        for review, user in reviews:
            review_responses.append(
                ReviewResponse(
                    id=review.id,
                    uuid=review.uuid,
                    user_uuid=user.uuid,
                    user_name=user.name,
                    user_avatar_url=user.avatar_url,
                    rating=review.rating,
                    review_text=review.review_text,
                    review_date=review.review_date
                )
            )
        return review_responses
    except Exception as e:
        logging.error(f"Error getting seller reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", response_model=ReviewResponse)
def create_review(
    review_create: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    try:
        logging.info(f"Received review data: {review_create.dict()}")
        review = review_crud.create_review(db, review_create, current_user.uuid)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create review. Either the deal doesn't exist, you're not the buyer, or a review already exists."
            )
        
        return ReviewResponse(
            id=review.id,
            uuid=review.uuid,
            user_uuid=current_user.uuid,
            user_name=current_user.name,
            user_avatar_url=current_user.avatar_url,
            rating=review.rating,
            review_text=review.review_text,
            review_date=review.review_date
        )
    except Exception as e:
        logging.error(f"Error creating review: {str(e)}")
        raise

@router.put("/{review_uuid}", response_model=ReviewResponse)
def update_review(
    review_uuid: UUID,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    try:
        review = db.query(ReviewModel).filter(ReviewModel.uuid == review_uuid).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        if review.user_uuid != current_user.uuid:
            raise HTTPException(status_code=403, detail="You can only edit your own reviews")
        
        for key, value in review_update.dict(exclude_unset=True).items():
            setattr(review, key, value)
        
        db.commit()
        db.refresh(review)
        
        seller_uuid = review.seller_uuid
        avg_rating = db.query(func.avg(ReviewModel.rating)).filter(ReviewModel.seller_uuid == seller_uuid).scalar() or 0
        seller = db.query(User).filter(User.uuid == seller_uuid).first()
        if seller:
            seller.rating = float(avg_rating)
            db.commit()
        
        return ReviewResponse(
            id=review.id,
            uuid=review.uuid,
            user_uuid=current_user.uuid,
            user_name=current_user.name,
            user_avatar_url=current_user.avatar_url,
            rating=review.rating,
            review_text=review.review_text,
            review_date=review.review_date
        )
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{review_uuid}")
def delete_review(
    review_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    # Find the review first
    review = db.query(ReviewModel).filter(ReviewModel.uuid == review_uuid).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if the user is the author of the review
    if review.user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="You can only delete your own reviews")
    
    if not review_crud.delete_review(db, review_uuid):
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}

@router.get("/deal/{deal_uuid}", response_model=ReviewResponse)
def get_deal_review(
    deal_uuid: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user)
):
    review = review_crud.get_deal_review(db, deal_uuid)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Get the reviewer's information
    reviewer = db.query(User).filter(User.uuid == review.user_uuid).first()
    if not reviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reviewer not found"
        )
    
    return ReviewResponse(
        id=review.id,
        uuid=review.uuid,
        user_uuid=reviewer.uuid,
        user_name=reviewer.name,
        user_avatar_url=reviewer.avatar_url,
        rating=review.rating,
        review_text=review.review_text,
        review_date=review.review_date
    )
