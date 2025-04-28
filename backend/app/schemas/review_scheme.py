from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from .user_scheme import *
# ================ Car ================

class Review(BaseModel):
    id: int
    user_id: int
    car_id: int
    review_text: Optional[str]
    rating: Optional[float]
    review_date: datetime

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    car_id: int
    rating: Optional[float] = None
    review_text: Optional[str] = None

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    review_text: Optional[str] = None

class ReviewDetailed(Review):
    user: UserMinimal
