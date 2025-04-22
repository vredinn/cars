# auth.py
from datetime import timedelta
from authx import AuthX, AuthXConfig
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import Field
from sqlalchemy.orm import Session
from crud import authenticate_user, get_user
from schemas import *
from database import get_db


auth_config = AuthXConfig(
    JWT_SECRET_KEY="super-secret-key",  # вынеси в .env
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=20),
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SAMESITE="lax",
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_REFRESH_COOKIE_NAME="refresh_token",
    JWT_COOKIE_CSRF_PROTECT=False,
)
auth = AuthX(config=auth_config)


router = APIRouter()


@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = str(db_user.id)
    response = JSONResponse(content={"message": "Logged in"})
    access_token = auth.create_access_token(uid=user_id)
    refresh_token = auth.create_refresh_token(uid=user_id)
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)
    return response


@router.post("/refresh")
def refresh_token(
    request: Request,
    response: Response,
):
    user_id = auth.get_current_subject(request)
    return user_id

    new_access = auth.create_access_token(uid=user_id)
    new_refresh = auth.create_refresh_token(uid=user_id)

    response = JSONResponse(content={"message": "Session refreshed"})
    auth.set_access_cookie(response, new_access)
    auth.set_refresh_cookie(response, new_refresh)

    return response


@router.post("/logout")
def logout(response: Response):
    auth.unset_cookies(response)
    return {"message": "Logged out"}


@router.get("/me")
def get_me(
    user_id: str = Depends(auth.access_token_required), db: Session = Depends(get_db)
):
    user = get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_admin(
    user_id: str = Depends(auth.access_token_required), db: Session = Depends(get_db)
):
    user = get_user(db, int(user_id))
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def require_user(
    user_id: str = Depends(auth.access_token_required), db: Session = Depends(get_db)
):
    user = get_user(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
