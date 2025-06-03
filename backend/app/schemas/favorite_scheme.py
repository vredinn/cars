from uuid import UUID
from pydantic import BaseModel

from .car_scheme import CarCard

class Favorite(BaseModel):
    id: int
    user_id: int
    car_id: int
    car: CarCard

    class Config:
        from_attributes = True

class FavoriteCreate(BaseModel):
    car_uuid: UUID