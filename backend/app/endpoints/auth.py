from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import Field
from sqlalchemy.orm import Session
from crud import authenticate_user, get_user_by_uuid, get_user_by_email, create_user
from schemas import *
from database import get_db
import security

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=409, detail="Email уже зарегистрирован")
    
    db_user = create_user(db, user)
    user_uuid = str(db_user.uuid)
    access_token = security.auth.create_access_token(uid=user_uuid)
    refresh_token = security.auth.create_refresh_token(uid=user_uuid)
    response = JSONResponse(content={"message": "Регистрация успешна"})
    security.auth.set_access_cookies(access_token, response)
    security.auth.set_refresh_cookies(refresh_token, response)
    return response

@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Данные для входа неверны")
    user_uuid = str(db_user.uuid)
    access_token = security.auth.create_access_token(uid=user_uuid)
    refresh_token = security.auth.create_refresh_token(uid=user_uuid)
    response = JSONResponse(content={"message": "Logged in"})
    security.auth.set_access_cookies(access_token, response)
    security.auth.set_refresh_cookies(refresh_token, response)
    return response

@router.post("/logout")
def logout(response: Response):
    security.auth.unset_cookies(response)
    return {"message": "Logged out"}


@router.post("/refresh")
def refresh(
    response: Response,
    request: Request,
    token: str = Depends(security.auth.refresh_token_required),
):
    
    new_access = security.auth.create_access_token(uid=token.sub)
    new_refresh = security.auth.create_refresh_token(uid=token.sub)
    response = JSONResponse(content={"message": "Session refreshed"})
    security.auth.set_access_cookies(new_access, response)
    security.auth.set_refresh_cookies(new_refresh, response)
    return response

@router.get("/me")
def get_me(
    user: User = Depends(security.require_user), db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

