from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

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
    name: str
    email: EmailStr
    phone: str
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
