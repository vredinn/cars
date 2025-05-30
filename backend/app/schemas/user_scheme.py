from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

# ================ User Schemas ================
class UserBase(BaseModel):
    uuid: UUID
    name: str
    email: EmailStr
    phone: str
    rating: float = Field(default=0.0, ge=0.0, le=5.0)

class UserWithImage(UserBase):
    avatar_url: Optional[str]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    phone: str
    password: str = Field(..., min_length=8)

    @field_validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', v):
            raise ValueError('Имя может содержать только буквы, пробелы и дефис')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[0-9]{10,15}$', v):
            raise ValueError('Неверный формат номера телефона')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', v):
            raise ValueError('Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, и цифры')
        return v

class User(UserWithImage):
    id: int
    registration_date: datetime
    is_admin: bool

    class Config:
        from_attributes = True


class UserMinimal(BaseModel):
    uuid: UUID
    name: str
    avatar_url: Optional[str]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: str
    email: str
    phone: str

    class Config:
        from_attributes = True

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str

    class Config:
        from_attributes = True

class UserChangeRights(BaseModel):
    is_admin: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', v):
            raise ValueError('Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, и цифры')
        return v
