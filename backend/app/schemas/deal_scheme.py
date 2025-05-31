from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class DealBase(BaseModel):
    pass

class DealCreate(BaseModel):
    car_uuid: UUID4
    buyer_uuid: UUID4

class DealInDB(DealBase):
    id: int
    uuid: UUID4
    car_id: int
    seller_id: int
    buyer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Deal(DealInDB):
    car_uuid: UUID4
    seller_uuid: UUID4
    buyer_uuid: UUID4 