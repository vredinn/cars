from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
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
    price: Decimal = Field(..., max_digits=12, decimal_places=2, gt=0)
    description: Optional[str] = Field(None, max_length=2000)
    body_type: BodyTypeEnum
    brand_id: int
    model_id: int
    drive_type: DriveTypeEnum
    transmission: TransmissionEnum
    fuel_type: FuelTypeEnum
    steering_side: SteeringSideEnum
    car_condition: CarConditionEnum
    engine_capacity: float = Field(..., gt=0, le=10.0)
    engine_power: int = Field(..., gt=0, le=2000)
    mileage: int = Field(..., ge=0)
    color: str = Field(..., min_length=2, max_length=50)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator('description')
    def validate_description(cls, v):
        if v and len(v.strip()) < 10:
            raise ValueError('Описание должно содержать минимум 10 символов')
        return v

    @field_validator('color')
    def validate_color(cls, v):
        if not v.strip():
            raise ValueError('Цвет не может быть пустым')
        return v.strip()

    @field_validator('year')
    def validate_year(cls, v):
        current_year = datetime.now().year
        if v > current_year + 1:
            raise ValueError('Год не может быть больше следующего года')
        if v < 1900:
            raise ValueError('Год не может быть меньше 1900')
        return v

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year + 1)
    price: Optional[Decimal] = Field(None, max_digits=12, decimal_places=2, gt=0)
    description: Optional[str] = Field(None, max_length=2000)
    body_type: Optional[BodyTypeEnum] = None
    brand_id: Optional[int] = None
    model_id: Optional[int] = None
    drive_type: Optional[DriveTypeEnum] = None
    transmission: Optional[TransmissionEnum] = None
    fuel_type: Optional[FuelTypeEnum] = None
    steering_side: Optional[SteeringSideEnum] = None
    car_condition: Optional[CarConditionEnum] = None
    engine_capacity: Optional[float] = Field(None, gt=0, le=10.0)
    engine_power: Optional[int] = Field(None, gt=0, le=2000)
    mileage: Optional[int] = Field(None, ge=0)
    color: Optional[str] = Field(None, min_length=2, max_length=50)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_sold: Optional[bool] = None

    @field_validator('description')
    def validate_description(cls, v):
        if v and len(v.strip()) < 10:
            raise ValueError('Описание должно содержать минимум 10 символов')
        return v

    @field_validator('color')
    def validate_color(cls, v):
        if v and not v.strip():
            raise ValueError('Цвет не может быть пустым')
        return v.strip() if v else v

    @field_validator('year')
    def validate_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v > current_year + 1:
                raise ValueError('Год не может быть больше следующего года')
            if v < 1900:
                raise ValueError('Год не может быть меньше 1900')
        return v

class Car(CarBase):
    uuid: UUID
    id: int
    user_id: int
    user_uuid: UUID
    is_sold: bool
    listing_date: datetime

    class Config:
        from_attributes = True

class CarDetailed(Car):
    images: List[CarImage]
    brand_name: str
    model_name: str
    user: User
    price_history: List[PriceHistoryBase]

class CarCard(Car):

    preview_image_url: Optional[str]  # первое изображение машины
    brand_name: str
    model_name: str

    class Config:
        from_attributes = True

class UserProfile(User):
    cars: List[CarCard]
    reviews: List[Review]