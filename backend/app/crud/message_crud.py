from sqlalchemy.orm import Session, selectinload
from uuid import uuid4

import models as m
from schemas import (
    MessageCreate
)

# ================ Message CRUD ================
def create_message(db: Session, msg: MessageCreate):
    obj = m.Message(**msg.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_messages(db: Session, user_id: int):
    return db.query(m.Message).filter((m.Message.sender_id == user_id) | (m.Message.receiver_id == user_id)).all()

def delete_message(db: Session, message_id: int):
    obj = db.query(m.Message).filter(m.Message.id == message_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True