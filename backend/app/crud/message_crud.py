from sqlalchemy.orm import Session, selectinload
from sqlalchemy import or_
from fastapi import HTTPException
from typing import List
from uuid import UUID

import models as m
from schemas.message_scheme import MessageCreate, Message

def create_message(db: Session, msg: MessageCreate, sender_uuid: UUID) -> m.Message:
    """
    Создание нового сообщения.
    Проверяет существование автомобиля и получателя.
    """
    # Проверяем, существует ли автомобиль
    car = db.query(m.Car).filter(m.Car.uuid == msg.car_uuid).first()
    if not car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")
    
    # Проверяем, существует ли получатель
    receiver = db.query(m.User).filter(m.User.uuid == msg.receiver_uuid).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Получатель не найден")
    
    # Проверяем, что отправитель не отправляет сообщение сам себе
    if sender_uuid == msg.receiver_uuid:
        raise HTTPException(status_code=400, detail="Нельзя отправить сообщение самому себе")
    
    # Создаем сообщение
    db_message = m.Message(
        car_uuid=msg.car_uuid,
        sender_uuid=sender_uuid,
        receiver_uuid=msg.receiver_uuid,
        message_text=msg.message_text
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Загружаем связанные данные
    db_message = (
        db.query(m.Message)
        .options(
            selectinload(m.Message.sender),
            selectinload(m.Message.receiver)
        )
        .filter(m.Message.id == db_message.id)
        .first()
    )
    return db_message

def get_user_chats(db: Session, user_uuid: UUID) -> List[m.Message]:
    """
    Получение списка чатов пользователя (уникальные комбинации car_uuid и собеседника).
    """
    messages = (
        db.query(m.Message)
        .options(
            selectinload(m.Message.sender),
            selectinload(m.Message.receiver),
            selectinload(m.Message.car)
        )
        .filter(or_(m.Message.sender_uuid == user_uuid, m.Message.receiver_uuid == user_uuid))
        .order_by(m.Message.sent_at.desc())
        .all()
    )
    
    # Группируем по car_uuid и собеседнику
    unique_chats = {}
    for msg in messages:
        other_user_uuid = msg.sender_uuid if msg.sender_uuid != user_uuid else msg.receiver_uuid
        chat_key = f"{msg.car_uuid}_{other_user_uuid}"
        if chat_key not in unique_chats:
            unique_chats[chat_key] = msg
    
    return list(unique_chats.values())

def get_chat_messages(db: Session, user_uuid: UUID, car_uuid: UUID, other_user_uuid: UUID) -> List[m.Message]:
    """
    Получение всех сообщений в чате для конкретного автомобиля и собеседника.
    """
    messages = (
        db.query(m.Message)
        .options(
            selectinload(m.Message.sender),
            selectinload(m.Message.receiver)
        )
        .filter(
            m.Message.car_uuid == car_uuid,
            or_(
                (m.Message.sender_uuid == user_uuid) & (m.Message.receiver_uuid == other_user_uuid),
                (m.Message.sender_uuid == other_user_uuid) & (m.Message.receiver_uuid == user_uuid)
            )
        )
        .order_by(m.Message.sent_at.asc())
        .all()
    )
    
    if not messages:
        car = db.query(m.Car).filter(m.Car.uuid == car_uuid).first()
        if not car:
            raise HTTPException(status_code=404, detail="Автомобиль не найден")
        user = db.query(m.User).filter(m.User.uuid == other_user_uuid).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return messages

def delete_message(db: Session, message_uuid: UUID, user_uuid: UUID) -> bool:
    """
    Удаление сообщения. Только отправитель может удалить.
    """
    message = (
        db.query(m.Message)
        .filter(m.Message.uuid == message_uuid, m.Message.sender_uuid == user_uuid)
        .first()
    )
    if not message:
        raise HTTPException(status_code=404, detail="Сообщение не найдено или нет прав")
    
    db.delete(message)
    db.commit()
    return True