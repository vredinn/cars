from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import os

from endpoints import (
    user, moderation, auth, brand, car, review, message, favorite, car_image, enum, car_model, deal
)


def create_app():
    app = FastAPI(
        title="API сайта для продажи автомобилей",
        swagger_ui_init_oauth={
            "usePkceWithAuthorizationCodeGrant": True,
            "useBasicAuthenticationWithAccessCodeGrant": True
        }
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    api_router = APIRouter(prefix="/api")

    api_router.include_router(auth.router)
    api_router.include_router(user.router)
    api_router.include_router(car.router)
    api_router.include_router(favorite.router)
    api_router.include_router(review.router)
    api_router.include_router(message.router)
    api_router.include_router(deal.router)
    api_router.include_router(brand.router)
    api_router.include_router(car_model.router)
    api_router.include_router(car_image.router)
    api_router.include_router(moderation.router)
    api_router.include_router(enum.router)
    app.router.include_router(api_router)

    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")    
    app.mount("/brand_logos", StaticFiles(directory="brand_logos"), name="brand_logos")
    os.makedirs("uploads", exist_ok=True)    
    os.makedirs("brand_logos", exist_ok=True)
    
    add_pagination(app)
    
    @app.get("/")
    def root():
        return {"message": "API is running"}

    return app