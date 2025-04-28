from typing import List, Optional
from pydantic import BaseModel, Field

# ================ Brand ================
class Brand(BaseModel):
    id: int
    name: str
    image_url: Optional[str]

    class Config:
        from_attributes = True

class BrandCreate(BaseModel):
    name: str
    image_url: Optional[str] = None
