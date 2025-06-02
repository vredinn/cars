from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi_pagination import Page, Params
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from PIL import Image
from pathlib import Path
import io
import uuid

from database import get_db
from schemas import *
import crud
import security
from config import settings

router = APIRouter(prefix="/users", tags=["Users"])

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_DIR = Path("uploads/avatars")
AVATAR_SIZE = 512  # размер аватарки 512x512

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db, user)

@router.get("/", response_model=List[UserAdmin])
def read_users(db: Session = Depends(get_db), current_user: User = Depends(security.require_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Только для администраторов")
    return crud.get_users(db)

@router.get("/search", response_model=List[UserAdmin])
def search_users(q: str, db: Session = Depends(get_db), current_user: User = Depends(security.require_user)):
    return crud.search_users(db, q)

@router.get("/{user_uuid}", response_model=UserProfile)
def read_user_by_uuid(user_uuid: UUID, db: Session = Depends(get_db)):
    user = crud.get_user_by_uuid(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_uuid}/cars", response_model=List[CarCard])
def read_user_cars(user_uuid: UUID, db: Session = Depends(get_db)):
    user = crud.get_user_by_uuid(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")    
    cars = user.cars
    if not cars:
        raise HTTPException(status_code=404, detail="Cars not found")
    return cars

@router.get("_popular", response_model=List[User])
def read_popular_users(db: Session = Depends(get_db)):
    return crud.get_popular_users(db)

@router.put("/{user_uuid}", response_model=User)
def update_user(
    user_uuid: UUID, 
    user_update: UserUpdate, 
    current_user: User = Depends(security.require_user),
    db: Session = Depends(get_db)
):
    # Проверяем права доступа
    if current_user.uuid != user_uuid and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет прав на изменение профиля")
    
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    if not user_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    updated = crud.update_user(db, user_id, user_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Не удалось обновить профиль")
    return updated

@router.put("/{user_uuid}/password")
def update_password(
    user_uuid: UUID,
    password_update: UserPasswordUpdate,
    current_user: User = Depends(security.require_user),
    db: Session = Depends(get_db)
):
    # Проверяем права доступа
    if current_user.uuid != user_uuid and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет прав на изменение пароля")
    
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    if not user_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Проверяем текущий пароль
    user = crud.get_user(db, user_id)
    if not crud.pwd_context.verify(password_update.current_password + settings.SALT, user.password):
        raise HTTPException(status_code=400, detail="Неверный текущий пароль")
    
    updated = crud.update_user_password(db, user_id, password_update.new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="Не удалось обновить пароль")
    return {"message": "Пароль успешно обновлен"}

@router.post("/{user_uuid}/avatar")
async def upload_avatar(
    user_uuid: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(security.require_user),
    db: Session = Depends(get_db)
):
    # Проверяем права доступа
    if current_user.uuid != user_uuid and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет прав на изменение аватара")
    
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    if not user_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Проверяем тип и размер файла
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Допустимы только JPEG и PNG")
    
    file.file.seek(0, io.SEEK_END)
    if file.file.tell() > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Слишком большой файл")
    file.file.seek(0)
    
    try:
        image = Image.open(file.file).convert("RGB")
        
        # Сохраняем пропорции изображения
        width, height = image.size
        if width > height:
            new_width = AVATAR_SIZE
            new_height = int(height * (AVATAR_SIZE / width))
        else:
            new_height = AVATAR_SIZE
            new_width = int(width * (AVATAR_SIZE / height))
            
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Если нужно создать квадратное изображение с сохранением пропорций,
        # можно создать белый фон и разместить изображение по центру:
        if False:  # Отключено, так как нам не нужен квадрат
            background = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), (255, 255, 255))
            offset = ((AVATAR_SIZE - new_width) // 2, (AVATAR_SIZE - new_height) // 2)
            background.paste(image, offset)
            image = background
        
        # Создаем директорию для аватаров пользователя
        user_dir = UPLOAD_DIR / str(user_uuid)
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Генерируем уникальное имя файла
        filename = f"{uuid.uuid4().hex}.webp"
        save_path = user_dir / filename
        
        # Сохраняем изображение
        image.save(save_path, "webp", quality=85)
        
        # Обновляем URL аватара в базе
        avatar_url = f"/uploads/avatars/{user_uuid}/{filename}"
        updated = crud.update_user_avatar(db, user_id, avatar_url)
        if not updated:
            raise HTTPException(status_code=404, detail="Не удалось обновить аватар")
        
        return {"avatar_url": avatar_url}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ошибка обработки изображения")

@router.put("/change_rights/{user_id}", response_model=User)
def update_user(user_id: int, user: UserChangeRights, db: Session = Depends(get_db)):
    updated = crud.user_change_rights(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_uuid}")
def delete_user(user_uuid: UUID, db: Session = Depends(get_db)):
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.delete("/{user_uuid}/avatar")
def delete_avatar(
    user_uuid: UUID,
    current_user: User = Depends(security.require_user),
    db: Session = Depends(get_db)
):
    # Проверяем права доступа
    if current_user.uuid != user_uuid and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Нет прав на изменение аватара")
    
    user_id = crud.get_user_id_by_uuid(db, user_uuid)
    if not user_id:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    updated = crud.update_user_avatar(db, user_id, None)
    if not updated:
        raise HTTPException(status_code=404, detail="Не удалось удалить аватар")
    
    return {"message": "Аватар успешно удален"}