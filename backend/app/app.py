from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import os

from endpoints import (
    user, moderation, auth, brand, car, review, message, favorite, car_image, saved_search, enum, car_model
)

def create_app():
    app = FastAPI(title="Car Ads API")

    # origins = ["http://localhost:5173", "http://localhost:3000", "*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешить всем (для разработки)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_router = APIRouter(prefix="/api")

    api_router.include_router(user.router)
    api_router.include_router(brand.router)
    api_router.include_router(car_model.router)
    api_router.include_router(car.router)
    api_router.include_router(review.router)
    api_router.include_router(message.router)
    api_router.include_router(favorite.router)
    api_router.include_router(car_image.router)
    api_router.include_router(saved_search.router)
    api_router.include_router(moderation.router)
    api_router.include_router(enum.router)
    api_router.include_router(auth.router)
    app.router.include_router(api_router)

    # статика
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")    
    app.mount("/brand_logos", StaticFiles(directory="brand_logos"), name="brand_logos")
    os.makedirs("uploads", exist_ok=True)    
    os.makedirs("brand_logos", exist_ok=True)
    

    add_pagination(app) 
    @app.get("/")
    def root():
        return {"message": "API is running"}

    return app