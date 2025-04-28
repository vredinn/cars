from datetime import datetime
from typing import List, Optional, Literal
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from .user_scheme import UserMinimal

# ================ Message ================
class Message(BaseModel):
    id: int
    car_id: int
    sender_id: int
    receiver_id: int
    message_text: str
    sent_at: datetime
    sender: UserMinimal
    receiver: UserMinimal


    class Config:
        from_attributes = True
        
class MessageCreate(BaseModel):
    receiver_id: int
    car_id: int
    message_text: str
