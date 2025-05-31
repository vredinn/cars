from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class ReviewBase(BaseModel):
    review_text: str = Field(..., min_length=1, max_length=1000)
    rating: float = Field(..., ge=1.0, le=5.0)

class ReviewCreate(BaseModel):
    deal_uuid: UUID
    review_text: str = Field(..., min_length=1, max_length=1000)
    rating: float = Field(..., ge=1.0, le=5.0)

class ReviewUpdate(BaseModel):
    review_text: str = Field(..., min_length=1, max_length=1000)
    rating: float = Field(..., ge=1.0, le=5.0)

class Review(BaseModel):
    id: int
    uuid: UUID
    user_uuid: UUID
    seller_uuid: UUID
    deal_uuid: UUID
    rating: float
    review_text: str
    review_date: datetime
    user_name: str
    user_avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class ReviewResponse(BaseModel):
    id: int
    uuid: UUID
    user_uuid: UUID
    user_name: str
    user_avatar_url: Optional[str] = None
    rating: float
    review_text: str
    review_date: datetime

    class Config:
        from_attributes = True 