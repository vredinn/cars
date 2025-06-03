from pydantic import BaseModel

class CarModel(BaseModel):
    id: int
    name: str
    brand_id: int

    class Config:
        from_attributes = True

class CarModelCreate(BaseModel):
    name: str
    brand_id: int
