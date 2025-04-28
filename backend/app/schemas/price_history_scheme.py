from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class PriceHistory(BaseModel):
    id: int
    car_id: int
    price: Decimal
    change_date: datetime

    class Config:
        from_attributes = True
