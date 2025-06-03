import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
from uuid import UUID
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from crud import get_user_by_uuid
from schemas import *
from database import get_db
from config import settings
import secrets
from starlette.middleware.base import BaseHTTPMiddleware

security = HTTPBearer(auto_error=False)

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 20
ALGORITHM = "HS256"

ACCESS_TOKEN_COOKIE = "access_token"
REFRESH_TOKEN_COOKIE = "refresh_token"
CSRF_ACCESS_TOKEN = "csrf_access_token"
CSRF_REFRESH_TOKEN = "csrf_refresh_token"

def create_token(data: dict, expires_delta: timedelta) -> tuple[str, str]:
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    csrf_token = secrets.token_urlsafe(32)
    to_encode.update({"csrf": csrf_token})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, csrf_token

def create_access_token(uid: str) -> tuple[str, str]:
    return create_token(
        {"sub": uid, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(uid: str) -> tuple[str, str]:
    return create_token(
        {"sub": uid, "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

def verify_token(token: str, csrf_token: str = None, token_type: str = "access") -> Dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != token_type:
            raise HTTPException(status_code=401, detail="Invalid token type")
        if csrf_token and payload.get("csrf") != csrf_token:
            raise HTTPException(status_code=401, detail="CSRF token mismatch")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def set_auth_cookies(response: Response, access_token: str, csrf_access: str, 
                    refresh_token: str = None, csrf_refresh: str = None):
    response.set_cookie(
        ACCESS_TOKEN_COOKIE,
        access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite="lax",
        secure=False 
    )
    response.set_cookie(
        CSRF_ACCESS_TOKEN,
        csrf_access,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=False,
        samesite="lax",
        secure=False
    )
    
    if refresh_token and csrf_refresh:
        response.set_cookie(
            REFRESH_TOKEN_COOKIE,
            refresh_token,
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=True,
            samesite="lax",
            secure=False
        )
        response.set_cookie(
            CSRF_REFRESH_TOKEN,
            csrf_refresh,
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            httponly=False,
            samesite="lax",
            secure=False
        )

def unset_auth_cookies(response: Response):
    response.delete_cookie(ACCESS_TOKEN_COOKIE)
    response.delete_cookie(REFRESH_TOKEN_COOKIE)
    response.delete_cookie(CSRF_ACCESS_TOKEN)
    response.delete_cookie(CSRF_REFRESH_TOKEN)

def get_token_from_cookies(request: Request, token_type: str = "access") -> Optional[str]:
    cookie_name = ACCESS_TOKEN_COOKIE if token_type == "access" else REFRESH_TOKEN_COOKIE
    return request.cookies.get(cookie_name)

def get_csrf_from_headers(request: Request) -> Optional[str]:
    return request.headers.get("X-CSRF-TOKEN")

async def get_current_user_from_token(
    request: Request,
    db: Session,
    auth: Optional[HTTPAuthorizationCredentials] = None
) -> Optional[User]:

    token = None
    if isinstance(auth, HTTPAuthorizationCredentials):
        token = auth.credentials

    if not token:
        token = get_token_from_cookies(request)
    
    csrf_token = get_csrf_from_headers(request)
        
    if not token:
        return None
        
    try:
        payload = verify_token(token, csrf_token)
        user = get_user_by_uuid(db, UUID(payload["sub"]))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        return None

async def require_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:

    auth = await security(request)
    user = await get_current_user_from_token(request, db, auth)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

async def optional_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    auth = await security(request)
    return await get_current_user_from_token(request, db, auth)

def require_admin(
    user: User = Depends(require_user)
) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:            # Skip CSRF check for auth endpoints that handle their own CSRF validation
            if request.url.path in ["/api/auth/login", "/api/auth/register", "/api/auth/refresh", "/api/auth/logout"]:
                return await call_next(request)
                
            csrf_token = request.headers.get("X-CSRF-TOKEN")
            if not csrf_token:
                return Response(
                    status_code=403,
                    content="CSRF token missing"
                )

            token = request.cookies.get(ACCESS_TOKEN_COOKIE)
            if not token:
                return Response(
                    status_code=401,
                    content="Authentication token missing"
                )

            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
                if payload.get("csrf") != csrf_token:
                    return Response(
                        status_code=403,
                        content="CSRF token mismatch"
                    )
            except jwt.ExpiredSignatureError:
                return Response(
                    status_code=401,
                    content="Token has expired"
                )
            except jwt.JWTError:
                return Response(
                    status_code=401,
                    content="Could not validate credentials"
                )

        return await call_next(request)
