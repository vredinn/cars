from pydantic import BaseModel
class CarImage(BaseModel):
    id: int
    car_id: int
    image_url: str

    class Config:
        from_attributes = True

class CarImageCreate(BaseModel):
    car_id: int
    image_url: str