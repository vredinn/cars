from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from .car_scheme import CarCard

class AdModerationBase(BaseModel):
    status: Literal["На проверке", "Одобрено", "Отклонено"]
    moderator_comment: Optional[str] = None

class AdModerationCreate(AdModerationBase):
    car_id: int

class AdModerationUpdate(AdModerationBase):
    pass

class AdModeration(AdModerationBase):
    id: int
    car_id: int
    moderation_date: datetime
    moderator_id: Optional[int] = None

    class Config:
        from_attributes = True

class AdModerationWithCar(AdModeration):
    car: CarCard

    class Config:
        from_attributes = True
