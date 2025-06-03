from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class UserMinimal(BaseModel):
    uuid: UUID
    name: str

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    car_uuid: UUID
    receiver_uuid: UUID
    message_text: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    uuid: UUID
    sender_uuid: UUID
    sent_at: datetime
    sender: Optional[UserMinimal] = None
    receiver: Optional[UserMinimal] = None

    class Config:
        from_attributes = True