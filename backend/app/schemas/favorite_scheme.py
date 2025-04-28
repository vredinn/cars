from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from .car_scheme import CarWithImages

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