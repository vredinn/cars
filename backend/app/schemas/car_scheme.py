from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from .enum_scheme import *
from .car_model_scheme import *
from .brand_scheme import *
from .user_scheme import *
from .car_image_scheme import *
from .price_history_scheme import *
from .review_scheme import *
# ================ Car ================
class CarBase(BaseModel):
    year: int = Field(..., ge=1900, le=datetime.now().year + 1)
    price: Decimal = Field(..., max_digits=12, decimal_places=2)
    description: Optional[str] = Field(None, max_length=2000)
    body_type: BodyTypeEnum
    brand_id: int
    model_id: int
    drive_type: DriveTypeEnum
    transmission: TransmissionEnum
    fuel_type: FuelTypeEnum
    steering_side: SteeringSideEnum
    car_condition: CarConditionEnum
    engine_capacity: float
    engine_power: int
    mileage: int
    color: str
    latitude: float
    longitude: float

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year + 1)
    price: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2)
    description: Optional[str] = Field(None, max_length=2000)
    body_type: Optional[BodyTypeEnum] = None
    brand_id: Optional[int] = None
    model_id: Optional[int] = None
    drive_type: Optional[DriveTypeEnum] = None
    transmission: Optional[TransmissionEnum] = None
    fuel_type: Optional[FuelTypeEnum] = None
    steering_side: Optional[SteeringSideEnum] = None
    car_condition: Optional[CarConditionEnum] = None
    engine_capacity: Optional[float] = None
    engine_power: Optional[int] = None
    mileage: Optional[int] = None
    color: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_sold: Optional[bool] = None

class Car(CarBase):
    uuid: UUID
    id: int
    user_id: int
    is_sold: bool
    listing_date: datetime

    class Config:
        from_attributes = True

class CarDetailed(Car):
    images: List[CarImage]
    user: User
    price_history: List[PriceHistoryBase]

class CarCard(Car):

    preview_image_url: Optional[str]  # первое изображение машины
    brand_name: str
    model_name: str

    class Config:
        from_attributes = True
