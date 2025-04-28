from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

# ================ Enums ================
DriveTypeEnum = Literal["Передний", "Задний", "Полный", "4x4"]
TransmissionEnum = Literal["Механика", "Автомат", "Вариатор", "Робот"]
FuelTypeEnum = Literal["Бензин", "Дизель", "Электро", "Гибрид"]
SteeringSideEnum = Literal["Левый", "Правый"]
CarConditionEnum = Literal["Новый", "Б/У", "После ремонта", "Повреждённый", "На запчасти"]
BodyTypeEnum = Literal[
    "Седан", "Хэтчбек", "Лифтбек", "Внедорожник", "Кроссовер", "Купе", "Кабриолет",
    "Универсал", "Минивэн", "Фургон", "Пикап", "Родстер", "Лимузин", "Тарга",
    "Фастбэк", "Микрокар"
]

# ================ User Schemas ================
class UserBase(BaseModel):
    uuid: UUID
    name: str
    email: EmailStr
    phone: str

class UserWithImage(UserBase):
    avatar_url: Optional[str]

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class User(UserWithImage):
    id: int
    registration_date: datetime
    is_admin: bool

    class Config:
        from_attributes = True


class UserMinimal(BaseModel):
    name: str
    avatar_url: Optional[str]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserChangeRights(BaseModel):
    is_admin: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ================ Brand & Model ================
class Brand(BaseModel):
    id: int
    name: str
    image_url: Optional[str]

    class Config:
        from_attributes = True

class BrandCreate(BaseModel):
    name: str
    image_url: Optional[str] = None

class CarModel(BaseModel):
    id: int
    name: str
    brand_id: int

    class Config:
        from_attributes = True

class CarModelCreate(BaseModel):
    name: str
    brand_id: int

# ================ Car ================
class CarBase(BaseModel):
    uuid: UUID
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
    id: int
    user_id: int
    is_sold: bool
    listing_date: datetime

    class Config:
        from_attributes = True

class CarImage(BaseModel):
    id: int
    car_id: int
    image_url: str

    class Config:
        from_attributes = True

class CarImageCreate(BaseModel):
    car_id: int
    image_url: str

class PriceHistory(BaseModel):
    id: int
    car_id: int
    price: Decimal
    change_date: datetime

    class Config:
        from_attributes = True

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

class CarWithImages(Car):
    images: List[CarImage]

class CarDetailed(CarWithImages):
    price_history: List[PriceHistory]
    reviews: List[ReviewDetailed]
    user: UserMinimal
    brand: Brand
    model: CarModel

class CarCard(CarBase):

    preview_image_url: Optional[str]  # первое изображение машины

    class Config:
        from_attributes = True

# ================ Favorite ================
class Favorite(BaseModel):
    id: int
    user_id: int
    car_id: int
    car: CarWithImages

    class Config:
        from_attributes = True

class FavoriteCreate(BaseModel):
    user_id: int
    car_id: int

# ================ Message ================
class Message(BaseModel):
    id: int
    car_id: int
    sender_id: int
    receiver_id: int
    message_text: str
    sent_at: datetime
    sender: UserMinimal
    receiver: UserMinimal


    class Config:
        from_attributes = True
        
class MessageCreate(BaseModel):
    receiver_id: int
    car_id: int
    message_text: str

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

# ================ SavedSearch ================
class SavedSearch(BaseModel):
    id: int
    user_id: int
    search_criteria: dict
    saved_at: datetime

    class Config:
        from_attributes = True

class SavedSearchCreate(BaseModel):
    user_id: int
    search_criteria: dict  