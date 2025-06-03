from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class PriceHistoryBase(BaseModel):
    price: Decimal
    change_date: datetime

class PriceHistory(PriceHistoryBase):
    id: int
    car_id: int

    class Config:
        from_attributes = True
