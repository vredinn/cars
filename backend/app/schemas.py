from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import condecimal, confloat, conint
from decimal import Decimal


# ================ User Schemas ================
class UserBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Full name of the user"
    )
    email: EmailStr = Field(..., description="User's email address")
    phone: str = Field(
        ..., min_length=5, max_length=20, description="User's phone number"
    )


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=8, max_length=100, description="User's password"
    )


class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Full name of the user"
    )
    email: Optional[EmailStr] = Field(None, description="User's email address")
    password: Optional[str] = Field(
        None, min_length=8, max_length=100, description="User's password"
    )
    phone: Optional[str] = Field(
        None, min_length=5, max_length=20, description="User's phone number"
    )
    avatar_url: Optional[str] = Field(None, description="URL to user's avatar image")
    is_admin: Optional[bool] = Field(None, description="Is user an administrator")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=8, max_length=100, description="User's password"
    )


class User(UserBase):
    id: int = Field(..., description="Unique user ID")
    registration_date: datetime = Field(
        ..., description="Date and time of user registration"
    )
    avatar_url: Optional[str] = Field(None, description="URL to user's avatar image")
    is_admin: bool = Field(False, description="Is user an administrator")

    class Config:
        from_attributes = True


# ================ Brand & Model Schemas ================
class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Brand name")


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int = Field(..., description="Unique brand ID")

    class Config:
        from_attributes = True


class ModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Model name")
    brand_id: int = Field(
        ..., gt=0, description="ID of the brand this model belongs to"
    )


class ModelCreate(ModelBase):
    pass


class Model(ModelBase):
    id: int = Field(..., description="Unique model ID")

    class Config:
        from_attributes = True


# ================ Category Schemas ================
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Category name")


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int = Field(..., description="Unique category ID")

    class Config:
        from_attributes = True


# ================ Car Property Schemas ================
class DriveTypeBase(BaseModel):
    type: str = Field(
        ..., min_length=1, max_length=20, description="Drive type (e.g., FWD, RWD, AWD)"
    )


class DriveTypeCreate(DriveTypeBase):
    pass


class DriveType(DriveTypeBase):
    id: int = Field(..., description="Unique drive type ID")

    class Config:
        from_attributes = True


class TransmissionBase(BaseModel):
    type: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Transmission type (e.g., Manual, Automatic)",
    )


class TransmissionCreate(TransmissionBase):
    pass


class Transmission(TransmissionBase):
    id: int = Field(..., description="Unique transmission ID")

    class Config:
        from_attributes = True


class FuelTypeBase(BaseModel):
    type: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Fuel type (e.g., Gasoline, Diesel, Electric)",
    )


class FuelTypeCreate(FuelTypeBase):
    pass


class FuelType(FuelTypeBase):
    id: int = Field(..., description="Unique fuel type ID")

    class Config:
        from_attributes = True


class SteeringSideBase(BaseModel):
    side: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Steering side (e.g., Left, Right)",
    )


class SteeringSideCreate(SteeringSideBase):
    pass


class SteeringSide(SteeringSideBase):
    id: int = Field(..., description="Unique steering side ID")

    class Config:
        from_attributes = True


class CarConditionBase(BaseModel):
    condition: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Car condition (e.g., New, Used, Damaged)",
    )


class CarConditionCreate(CarConditionBase):
    pass


class CarCondition(CarConditionBase):
    id: int = Field(..., description="Unique car condition ID")

    class Config:
        from_attributes = True


# ================ Car Schemas ================
class CarBase(BaseModel):
    year: int = Field(
        ...,
        ge=1900,
        le=datetime.now().year + 1,
        description="Manufacturing year of the car",
    )
    price: Decimal = Field(
        ..., max_digits=12, decimal_places=2, description="Current price of the car"
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="Detailed description of the car"
    )
    category_id: int = Field(..., gt=0, description="ID of the car category")
    brand_id: int = Field(..., gt=0, description="ID of the car brand")
    model_id: int = Field(..., gt=0, description="ID of the car model")
    drive_type_id: int = Field(..., gt=0, description="ID of the drive type")
    transmission_id: int = Field(..., gt=0, description="ID of the transmission type")
    fuel_type_id: int = Field(..., gt=0, description="ID of the fuel type")
    steering_side_id: int = Field(..., gt=0, description="ID of the steering side")
    car_condition_id: int = Field(..., gt=0, description="ID of the car condition")
    engine_capacity: float = Field(..., gt=0, description="Engine capacity in liters")
    engine_power: int = Field(..., gt=0, description="Engine power in horsepower")
    mileage: int = Field(..., ge=0, description="Car mileage in kilometers")
    color: str = Field(..., min_length=1, max_length=30, description="Color of the car")
    latitude: float = Field(
        ..., ge=-90, le=90, description="Geographical latitude of the car location"
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Geographical longitude of the car location"
    )


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    year: Optional[int] = Field(
        None,
        ge=1900,
        le=datetime.now().year + 1,
        description="Manufacturing year of the car",
    )
    price: Optional[Decimal] = Field(
        None, max_digits=12, decimal_places=2, description="Current price of the car"
    )
    description: Optional[str] = Field(
        None, max_length=2000, description="Detailed description of the car"
    )
    category_id: Optional[int] = Field(None, gt=0, description="ID of the car category")
    brand_id: Optional[int] = Field(None, gt=0, description="ID of the car brand")
    model_id: Optional[int] = Field(None, gt=0, description="ID of the car model")
    drive_type_id: Optional[int] = Field(None, gt=0, description="ID of the drive type")
    transmission_id: Optional[int] = Field(
        None, gt=0, description="ID of the transmission type"
    )
    fuel_type_id: Optional[int] = Field(None, gt=0, description="ID of the fuel type")
    steering_side_id: Optional[int] = Field(
        None, gt=0, description="ID of the steering side"
    )
    car_condition_id: Optional[int] = Field(
        None, gt=0, description="ID of the car condition"
    )
    engine_capacity: Optional[float] = Field(
        None, gt=0, description="Engine capacity in liters"
    )
    engine_power: Optional[int] = Field(
        None, gt=0, description="Engine power in horsepower"
    )
    is_sold: Optional[bool] = Field(None, description="Is the car sold")
    mileage: Optional[int] = Field(None, ge=0, description="Car mileage in kilometers")
    color: Optional[str] = Field(
        None, min_length=1, max_length=30, description="Color of the car"
    )
    latitude: Optional[float] = Field(
        None, ge=-90, le=90, description="Geographical latitude of the car location"
    )
    longitude: Optional[float] = Field(
        None, ge=-180, le=180, description="Geographical longitude of the car location"
    )


class Car(CarBase):
    id: int = Field(..., description="Unique car ID")
    user_id: int = Field(..., gt=0, description="ID of the user who listed the car")
    is_sold: bool = Field(False, description="Is the car sold")
    listing_date: datetime = Field(
        ..., description="Date and time when the car was listed"
    )
    user: User = Field(..., description="User who listed the car")
    brand: Brand = Field(..., description="Car brand")
    model: Model = Field(..., description="Car model")
    category: Category = Field(..., description="Car category")
    drive_type: DriveType = Field(..., description="Drive type")
    transmission: Transmission = Field(..., description="Transmission type")
    fuel_type: FuelType = Field(..., description="Fuel type")
    steering_side: SteeringSide = Field(..., description="Steering side")
    car_condition: CarCondition = Field(..., description="Car condition")

    class Config:
        from_attributes = True


class CarWithImages(Car):
    images: List["CarImage"] = Field(..., description="List of car images")


class CarWithDetails(CarWithImages):
    price_history: List["PriceHistory"] = Field(
        ..., description="Price history of the car"
    )
    reviews: List["Review"] = Field(..., description="Reviews of the car")


# ================ Favorite Schemas ================
class FavoriteBase(BaseModel):
    user_id: int = Field(..., gt=0, description="ID of the user who favorited the car")
    car_id: int = Field(..., gt=0, description="ID of the favorited car")


class FavoriteCreate(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    id: int = Field(..., description="Unique favorite entry ID")
    car: Car = Field(..., description="Favorited car details")

    class Config:
        from_attributes = True


# ================ Message Schemas ================
class MessageBase(BaseModel):
    car_id: int = Field(..., gt=0, description="ID of the car the message is about")
    receiver_id: int = Field(..., gt=0, description="ID of the message receiver")
    message_text: str = Field(
        ..., min_length=1, max_length=2000, description="Message content"
    )


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int = Field(..., description="Unique message ID")
    sender_id: int = Field(..., gt=0, description="ID of the message sender")
    sent_at: datetime = Field(
        ..., description="Date and time when the message was sent"
    )
    car: Car = Field(..., description="Car details the message is about")
    sender: User = Field(..., description="Message sender details")
    receiver: User = Field(..., description="Message receiver details")

    class Config:
        from_attributes = True


# ================ Ad Moderation Schemas ================
class AdModerationBase(BaseModel):
    car_id: int = Field(..., gt=0, description="ID of the car being moderated")
    status: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Moderation status (e.g., Pending, Approved, Rejected)",
    )
    moderator_comment: Optional[str] = Field(
        None, max_length=1000, description="Comment from the moderator"
    )


class AdModerationCreate(AdModerationBase):
    pass


class AdModerationUpdate(BaseModel):
    status: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        description="Moderation status (e.g., Pending, Approved, Rejected)",
    )
    moderator_comment: Optional[str] = Field(
        None, max_length=1000, description="Comment from the moderator"
    )


class AdModeration(AdModerationBase):
    id: int = Field(..., description="Unique moderation entry ID")
    moderation_date: datetime = Field(..., description="Date and time of moderation")
    car: Car = Field(..., description="Car details being moderated")

    class Config:
        from_attributes = True


# ================ Saved Search Schemas ================
class SavedSearchBase(BaseModel):
    user_id: int = Field(..., gt=0, description="ID of the user who saved the search")
    search_criteria: dict = Field(..., description="Search criteria as a dictionary")


class SavedSearchCreate(SavedSearchBase):
    pass


class SavedSearch(SavedSearchBase):
    id: int = Field(..., description="Unique saved search ID")
    saved_at: datetime = Field(
        ..., description="Date and time when the search was saved"
    )

    class Config:
        from_attributes = True


# ================ Review Schemas ================
class ReviewBase(BaseModel):
    car_id: int = Field(..., gt=0, description="ID of the car being reviewed")
    review_text: Optional[str] = Field(
        None, max_length=2000, description="Text content of the review"
    )
    rating: Optional[int] = Field(
        None, ge=1, le=5, description="Rating from 1 to 5 stars"
    )


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    review_text: Optional[str] = Field(
        None, max_length=2000, description="Text content of the review"
    )
    rating: Optional[int] = Field(
        None, ge=1, le=5, description="Rating from 1 to 5 stars"
    )


class Review(ReviewBase):
    id: int = Field(..., description="Unique review ID")
    user_id: int = Field(..., gt=0, description="ID of the user who wrote the review")
    review_date: datetime = Field(
        ..., description="Date and time when the review was written"
    )
    user: User = Field(..., description="User who wrote the review")
    car: Car = Field(..., description="Car being reviewed")

    class Config:
        from_attributes = True


# ================ Price History Schemas ================
class PriceHistoryBase(BaseModel):
    car_id: int = Field(..., gt=0, description="ID of the car with price history")
    price: Decimal = Field(
        ..., max_digits=12, decimal_places=2, description="Price at this history point"
    )


class PriceHistoryCreate(PriceHistoryBase):
    pass


class PriceHistory(PriceHistoryBase):
    id: int = Field(..., description="Unique price history entry ID")
    change_date: datetime = Field(..., description="Date and time of the price change")
    car: Car = Field(..., description="Car details with price history")

    class Config:
        from_attributes = True


# ================ Car Image Schemas ================
class CarImageBase(BaseModel):
    car_id: int = Field(..., gt=0, description="ID of the car this image belongs to")
    image_url: str = Field(..., max_length=500, description="URL of the car image")


class CarImageCreate(CarImageBase):
    pass


class CarImage(CarImageBase):
    id: int = Field(..., description="Unique car image ID")
    car: Car = Field(..., description="Car details this image belongs to")

    class Config:
        from_attributes = True


# Update forward references for nested models
CarWithImages.model_rebuild()
CarWithDetails.model_rebuild()
