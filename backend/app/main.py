import uuid
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime
from database import get_db
from schemas import *
import crud
import auth
import authx

app = FastAPI(title="cars-api", version="0.1.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Монтируем папку uploads как статическую
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Настройки для загрузки изображений
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ================ User Endpoints ================
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db=db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


# ================ Brand Endpoints ================
@app.post("/brands/", response_model=Brand)
def create_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    return crud.create_brand(db=db, brand=brand)


@app.get("/brands/", response_model=List[Brand])
def read_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_brands(db, skip=skip, limit=limit)


@app.get("/brands/{brand_id}", response_model=Brand)
def read_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id=brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand


@app.put("/brands/{brand_id}", response_model=Brand)
def update_brand(brand_id: int, name: str, db: Session = Depends(get_db)):
    db_brand = crud.update_brand(db=db, brand_id=brand_id, brand_name=name)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand


@app.delete("/brands/{brand_id}")
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    if not crud.delete_brand(db=db, brand_id=brand_id):
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"message": "Brand deleted successfully"}


# ================ Model Endpoints ================
@app.post("/models/", response_model=Model)
def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    return crud.create_model(db=db, model=model)


@app.get("/models/", response_model=List[Model])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_models_by_brand(db, brand_id=None, skip=skip, limit=limit)


@app.get("/brands/{brand_id}/models/", response_model=List[Model])
def read_models_by_brand(
    brand_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_models_by_brand(db, brand_id=brand_id, skip=skip, limit=limit)


@app.get("/models/{model_id}", response_model=Model)
def read_model(model_id: int, db: Session = Depends(get_db)):
    db_model = crud.get_model(db, model_id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model


@app.put("/models/{model_id}", response_model=Model)
def update_model(model_id: int, model: ModelCreate, db: Session = Depends(get_db)):
    db_model = crud.update_model(db=db, model_id=model_id, model=model)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model


@app.delete("/models/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    if not crud.delete_model(db=db, model_id=model_id):
        raise HTTPException(status_code=404, detail="Model not found")
    return {"message": "Model deleted successfully"}


# ================ Car Endpoints ================
@app.post("/cars/", response_model=Car)
def create_car(car: CarCreate, user_id: int = 1, db: Session = Depends(get_db)):
    return crud.create_car(db=db, car=car, user_id=user_id)


@app.get("/cars/", response_model=List[Car])
def read_cars(
    skip: int = 0,
    limit: int = 100,
    brand_id: Optional[int] = None,
    model_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
):
    filters = {}
    if brand_id:
        filters["brand_id"] = brand_id
    if model_id:
        filters["model_id"] = model_id
    if min_price:
        filters["min_price"] = min_price
    if max_price:
        filters["max_price"] = max_price

    return crud.get_cars(db, skip=skip, limit=limit, filters=filters)


@app.get("/cars/{car_id}", response_model=Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = crud.update_car(db=db, car_id=car_id, car_update=car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    if not crud.delete_car(db=db, car_id=car_id):
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}


# ================ Favorite Endpoints ================
@app.post("/favorites/", response_model=Favorite)
def create_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    return crud.create_favorite(db=db, favorite=favorite)


@app.get("/users/{user_id}/favorites/", response_model=List[Favorite])
def read_favorites(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_favorites_by_user(db, user_id=user_id, skip=skip, limit=limit)


@app.delete("/favorites/{user_id}/{car_id}")
def delete_favorite(user_id: int, car_id: int, db: Session = Depends(get_db)):
    if not crud.delete_favorite(db=db, user_id=user_id, car_id=car_id):
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite deleted successfully"}


# ================ Message Endpoints ================
@app.post("/messages/", response_model=Message)
def create_message(
    message: MessageCreate, sender_id: int = 1, db: Session = Depends(get_db)
):
    return crud.create_message(db=db, message=message, sender_id=sender_id)


@app.get("/users/{user_id}/messages/", response_model=List[Message])
def read_messages(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_messages(db, user_id=user_id, skip=skip, limit=limit)


# ================ Ad Moderation Endpoints ================
@app.post("/moderations/", response_model=AdModeration)
def create_moderation(moderation: AdModerationCreate, db: Session = Depends(get_db)):
    return crud.create_moderation_entry(db=db, moderation=moderation)


@app.get("/moderations/", response_model=List[AdModeration])
def read_moderations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_moderation_entries(db, skip=skip, limit=limit)


@app.put("/moderations/{moderation_id}", response_model=AdModeration)
def update_moderation(
    moderation_id: int, moderation: AdModerationUpdate, db: Session = Depends(get_db)
):
    db_moderation = crud.update_moderation_entry(
        db=db, moderation_id=moderation_id, moderation_update=moderation
    )
    if db_moderation is None:
        raise HTTPException(status_code=404, detail="Moderation entry not found")
    return db_moderation


# ================ Review Endpoints ================
@app.post("/reviews/", response_model=Review)
def create_review(
    review: ReviewCreate, user_id: int = 1, db: Session = Depends(get_db)
):
    return crud.create_review(db=db, review=review, user_id=user_id)


@app.get("/cars/{car_id}/reviews/", response_model=List[Review])
def read_reviews_by_car(
    car_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_reviews_by_car(db, car_id=car_id, skip=skip, limit=limit)


@app.put("/reviews/{review_id}", response_model=Review)
def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud.update_review(db=db, review_id=review_id, review_update=review)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    if not crud.delete_review(db=db, review_id=review_id):
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}


# ================ Price History Endpoints ================
@app.get("/cars/{car_id}/price-history/", response_model=List[PriceHistory])
def read_price_history(
    car_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_price_history(db, car_id=car_id, skip=skip, limit=limit)


# ================ Car Image Endpoints ================
@app.post("/cars/{car_id}/images/", response_model=CarImage)
async def upload_car_image(
    car_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    # Проверяем существование автомобиля
    db_car = crud.get_car(db, car_id=car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Проверяем расширение файла
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_ext = os.path.splitext(file.filename.lower())[1]
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}",
        )

    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    upload_dir = "uploads/cars"
    os.makedirs(upload_dir, exist_ok=True)  # Создаем папку, если не существует
    file_path = os.path.join(upload_dir, unique_filename)

    # Сохраняем файл
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        await file.close()

    # Создаем запись в БД
    image_url = f"/uploads/cars/{unique_filename}"
    db_image = crud.create_car_image(
        db=db, car_image=CarImageCreate(car_id=car_id, image_url=image_url)
    )

    return db_image


@app.get("/cars/{car_id}/images/", response_model=List[CarImage])
def get_car_images(car_id: int, db: Session = Depends(get_db)):
    # Проверяем существование автомобиля
    db_car = crud.get_car(db, car_id=car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")

    return crud.get_car_images(db, car_id=car_id)


@app.delete("/images/{image_id}")
def delete_car_image(image_id: int, db: Session = Depends(get_db)):
    if not crud.delete_car_image(db=db, image_id=image_id):
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}
