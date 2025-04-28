from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

# ================ SavedSearch ================
class SavedSearch(BaseModel):
    id: int
    user_id: int
    search_criteria: dict
    saved_at: datetime

    class Config:
        from_attributes = True

class SavedSearchCreate(BaseModel):
    user_id: int
    search_criteria: dict  