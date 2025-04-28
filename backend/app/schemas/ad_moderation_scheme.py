from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from .car_scheme import CarWithImages

# ================ AdModeration ================
class AdModeration(BaseModel):
    id: int
    car_id: int
    status: str
    moderator_comment: Optional[str]
    moderation_date: datetime
    car: CarWithImages

    class Config:
        from_attributes = True

class AdModerationCreate(BaseModel):
    car_id: int
    is_approved: bool
    moderator_comment: Optional[str] = None

class AdModerationUpdate(BaseModel):
    is_approved: Optional[bool] = None
    moderator_comment: Optional[str] = None
