from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class PriceHistoryBase(BaseModel):
    price: Decimal
    change_date: datetime

class PriceHistory(PriceHistoryBase):
    id: int
    car_id: int

    class Config:
        from_attributes = True
