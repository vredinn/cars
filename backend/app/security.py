from datetime import timedelta
from authx import AuthX, AuthXConfig
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from crud import get_user_by_uuid
from schemas import *
from database import get_db
from config import settings

auth_config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=20),
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SAMESITE="lax",
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_REFRESH_COOKIE_NAME="refresh_token",
    JWT_COOKIE_SECURE=False, 
)
auth = AuthX(config=auth_config)

def require_user(token: str = Depends(auth.access_token_required), db: Session = Depends(get_db)):
    user = get_user_by_uuid(db, UUID(token.sub))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_admin(user: dict = Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Требуются права администратора")
    return user
