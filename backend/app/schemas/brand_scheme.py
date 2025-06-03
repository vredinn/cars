from typing import Optional
from pydantic import BaseModel

class Brand(BaseModel):
    id: int
    name: str
    image_url: Optional[str]

    class Config:
        from_attributes = True

class BrandCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
