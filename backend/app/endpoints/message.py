from typing import List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import json
from uuid import UUID

from database import get_db
from schemas.message_scheme import Message, MessageCreate
import crud
import models as m
from security import require_user

router = APIRouter(prefix="/messages", tags=["Сообщения"])

# Хранилище активных WebSocket-соединений
connected_clients = {}

@router.get("/user/{user_uuid}", response_model=List[Message])
def get_user_chats(user_uuid: UUID, db: Session = Depends(get_db), current_user: m.User = Depends(require_user)):
    """
    Получение списка чатов пользователя.
    """
    if current_user.uuid != user_uuid:
        raise HTTPException(status_code=403, detail="Нет прав для просмотра чужих чатов")
    return crud.get_user_chats(db, user_uuid)

@router.get("/chat/{car_uuid}/{other_user_uuid}", response_model=List[Message])
def get_chat_messages(car_uuid: UUID, other_user_uuid: UUID, db: Session = Depends(get_db), current_user: m.User = Depends(require_user)):
    """
    Получение сообщений в чате для автомобиля и собеседника.
    """
    return crud.get_chat_messages(db, current_user.uuid, car_uuid, other_user_uuid)

@router.post("/", response_model=Message)
def create_message(message: MessageCreate, db: Session = Depends(get_db), current_user: m.User = Depends(require_user)):
    """
    Создание нового сообщения.
    """
    return crud.create_message(db, message, current_user.uuid)

@router.delete("/{message_uuid}", response_model=bool)
def delete_message(message_uuid: UUID, db: Session = Depends(get_db), current_user: m.User = Depends(require_user)):
    """
    Удаление сообщения.
    """
    return crud.delete_message(db, message_uuid, current_user.uuid)

@router.websocket("/ws/{user_uuid}/{car_uuid}/{other_user_uuid}")
async def websocket_endpoint(websocket: WebSocket, user_uuid: UUID, car_uuid: UUID, other_user_uuid: UUID):
    """
    WebSocket для чата в реальном времени.
    """
    db = next(get_db())

    await websocket.accept()
    chat_key = f"{user_uuid}_{car_uuid}_{other_user_uuid}"
    connected_clients[chat_key] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Получено сообщение: {data}")
            message_data = json.loads(data)
            
            db = next(get_db())
            try:
                msg_create = MessageCreate(
                    car_uuid=car_uuid,
                    receiver_uuid=other_user_uuid,
                    message_text=message_data["message_text"]
                )
                db_message = crud.create_message(db, msg_create, user_uuid)
                
                # Формируем ответ
                response = {
                    "id": db_message.id,
                    "uuid": str(db_message.uuid),
                    "car_uuid": str(db_message.car_uuid),
                    "sender_uuid": str(db_message.sender_uuid),
                    "receiver_uuid": str(db_message.receiver_uuid),
                    "message_text": db_message.message_text,
                    "sent_at": db_message.sent_at.isoformat(),
                    "sender": {
                        "uuid": str(db_message.sender.uuid),
                        "name": db_message.sender.name
                    },
                    "receiver": {
                        "uuid": str(db_message.receiver.uuid),
                        "name": db_message.receiver.name
                    }
                }
                
                # Отправляем сообщение обоим
                if chat_key in connected_clients:
                    await connected_clients[chat_key].send_json(response)
                reverse_chat_key = f"{other_user_uuid}_{car_uuid}_{user_uuid}"
                if reverse_chat_key in connected_clients:
                    await connected_clients[reverse_chat_key].send_json(response)
            finally:
                db.close()
    except WebSocketDisconnect:
        print(f"WebSocket отключен: {chat_key}")
    except Exception as e:
        print(f"Ошибка WebSocket: {e}")
    finally:
        if chat_key in connected_clients:
            del connected_clients[chat_key]
        await websocket.close()
        print(f"WebSocket закрыт: {chat_key}")