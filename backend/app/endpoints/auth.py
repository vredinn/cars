from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from crud import authenticate_user, get_user_by_email, create_user
from schemas import *
from database import get_db
import security

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

@router.post("/register", 
    responses={
        200: {"description": "Регистрация успешна"},
        409: {"description": "Email уже зарегистрирован"}
    },
    description="Зарегистрировать нового пользователя."
)
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=409, detail="Email уже зарегистрирован")
    
    db_user = create_user(db, user)
    user_uuid = str(db_user.uuid)
    
    access_token, csrf_access = security.create_access_token(user_uuid)
    refresh_token, csrf_refresh = security.create_refresh_token(user_uuid)
    
    response = JSONResponse(content={
        "message": "Регистрация успешна"
    })
    security.set_auth_cookies(
        response, 
        access_token, 
        csrf_access, 
        refresh_token, 
        csrf_refresh
    )
    return response

@router.post("/login",
    description="Вход пользователя с использованием электронной почты и пароля.",
    response_model=UserLogin,
)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Данные для входа неверны")
    
    user_uuid = str(db_user.uuid)
    
    access_token, csrf_access = security.create_access_token(user_uuid)
    refresh_token, csrf_refresh = security.create_refresh_token(user_uuid)
    
    response = JSONResponse(content={
        "message": "Успешно вошли в систему",
    })
    security.set_auth_cookies(
        response, 
        access_token, 
        csrf_access, 
        refresh_token, 
        csrf_refresh
    )
    return response

@router.post("/logout",
    responses={
        200: {"description": "Успешно вышли из системы"},
        401: {"description": "Не аутентифицирован"}
    },
    description="Выход пользователя из системы. Удаляет токены и CSRF-токены из cookies."
)
def logout(response: Response, user: User = Depends(security.require_user)):
    security.unset_auth_cookies(response)
    return {"message": "Успешно вышли из системы"}


@router.post("/refresh",
    responses={
        200: {"description": "Сессия обновлена"},
        401: {"description": "Нет действительного refresh токена или CSRF токена"}
    },
    description="Обновление сессии пользователя. Используется для получения новых access и refresh токенов, если текущий refresh действителен."
)
def refresh(request: Request, response: Response):
    refresh_token = security.get_token_from_cookies(request, "refresh")
    csrf_token = security.get_csrf_from_headers(request)
    
    if not refresh_token or not csrf_token:
        raise HTTPException(status_code=401, detail="Нет действительного refresh токена или CSRF токена")
    
    payload = security.verify_token(refresh_token, csrf_token, "refresh")
    user_uuid = payload["sub"]
    
    access_token, csrf_access = security.create_access_token(user_uuid)
    refresh_token, csrf_refresh = security.create_refresh_token(user_uuid)
    
    response = JSONResponse(content={
        "message": "Сессия обновлена"
    })
    security.set_auth_cookies(
        response,
        access_token,
        csrf_access,
        refresh_token,
        csrf_refresh
    )
    return response

@router.get("/me",
    responses={
        200: {"model": User, "description": "Информация о текущем пользователе"},
        401: {"description": "Не аутентифицирован"},
    },
    description="Получить информацию о текущем пользователе."
)
def get_me(user: User = Depends(security.require_user)):
    return user

