from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
# ================ Car Image ================
class CarImage(BaseModel):
    id: int
    car_id: int
    image_url: str

    class Config:
        from_attributes = True

class CarImageCreate(BaseModel):
    car_id: int
    image_url: str