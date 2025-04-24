from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page

from database import get_db
from schemas import Message, MessageCreate
import crud

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/user/{user_id}", response_model=List[Message])
def get_messages(user_id: int, db: Session = Depends(get_db)):
    return crud.get_messages(db, user_id)

@router.post("/", response_model=Message)
def create_message(message: MessageCreate, db: Session = Depends(get_db), sender_id: int = 1):
    return crud.create_message(db, message, sender_id)
