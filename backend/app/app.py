from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
import os

from endpoints import (
    user, moderation, auth, brand, car, review, message, favorite, car_image, saved_search, enum, car_model
)

def create_app():
    app = FastAPI(title="Car Ads API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешить всем (для разработки)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user.router)
    app.include_router(brand.router)
    app.include_router(car_model.router)
    app.include_router(car.router)
    app.include_router(review.router)
    app.include_router(message.router)
    app.include_router(favorite.router)
    app.include_router(car_image.router)
    app.include_router(saved_search.router)
    app.include_router(moderation.router)
    app.include_router(enum.router)
    app.include_router(auth.router)

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