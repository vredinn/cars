from datetime import datetime
from typing import List, Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from schemas import *
from models import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ================ User CRUD ================
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        registration_date=datetime.now(),
        is_admin=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    if "password" in update_data:
        hashed_password = pwd_context.hash(update_data["password"])
        del update_data["password"]
        update_data["password"] = hashed_password

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user


# ================ Brand CRUD ================
def get_brand(db: Session, brand_id: int) -> Optional[Brand]:
    return db.query(Brand).filter(Brand.id == brand_id).first()


def get_brands(db: Session, skip: int = 0, limit: int = 100) -> List[Brand]:
    return db.query(Brand).offset(skip).limit(limit).all()


def create_brand(db: Session, brand: BrandCreate) -> Brand:
    db_brand = Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


def update_brand(db: Session, brand_id: int, brand_name: str) -> Optional[Brand]:
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        return None
    db_brand.name = brand_name
    db.commit()
    db.refresh(db_brand)
    return db_brand


def delete_brand(db: Session, brand_id: int) -> bool:
    db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not db_brand:
        return False
    db.delete(db_brand)
    db.commit()
    return True


# ================ Model CRUD ================
def get_model(db: Session, model_id: int) -> Optional[Model]:
    return db.query(Model).filter(Model.id == model_id).first()


def get_models_by_brand(
    db: Session, brand_id: int, skip: int = 0, limit: int = 100
) -> List[Model]:
    return (
        db.query(Model)
        .filter(Model.brand_id == brand_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_model(db: Session, model: ModelCreate) -> Model:
    db_model = Model(name=model.name, brand_id=model.brand_id)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def update_model(db: Session, model_id: int, model: ModelCreate) -> Optional[Model]:
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        return None
    db_model.name = model.name
    db_model.brand_id = model.brand_id
    db.commit()
    db.refresh(db_model)
    return db_model


def delete_model(db: Session, model_id: int) -> bool:
    db_model = db.query(Model).filter(Model.id == model_id).first()
    if not db_model:
        return False
    db.delete(db_model)
    db.commit()
    return True


# ================ Car CRUD ================
def get_car(db: Session, car_id: int) -> Optional[Car]:
    return db.query(Car).filter(Car.id == car_id).first()


def get_cars(
    db: Session, skip: int = 0, limit: int = 100, filters: dict = None
) -> List[Car]:
    query = db.query(Car)

    if filters:
        # Пример фильтрации (можно расширить)
        if "brand_id" in filters:
            query = query.filter(Car.brand_id == filters["brand_id"])
        if "model_id" in filters:
            query = query.filter(Car.model_id == filters["model_id"])
        if "min_price" in filters:
            query = query.filter(Car.price >= filters["min_price"])
        if "max_price" in filters:
            query = query.filter(Car.price <= filters["max_price"])
        if "is_sold" in filters:
            query = query.filter(Car.is_sold == filters["is_sold"])

    return query.offset(skip).limit(limit).all()


def create_car(db: Session, car: CarCreate, user_id: int) -> Car:
    db_car = Car(
        **car.dict(), user_id=user_id, listing_date=datetime.now(), is_sold=False
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)

    # Создаем запись в истории цен
    create_price_history(db, car_id=db_car.id, price=car.price)

    return db_car


def update_car(db: Session, car_id: int, car_update: CarUpdate) -> Optional[Car]:
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        return None

    update_data = car_update.dict(exclude_unset=True)

    # Если обновляется цена, добавляем запись в историю цен
    if "price" in update_data and update_data["price"] != db_car.price:
        create_price_history(db, car_id=car_id, price=update_data["price"])

    for field, value in update_data.items():
        setattr(db_car, field, value)

    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: int) -> bool:
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        return False
    db.delete(db_car)
    db.commit()
    return True


# ================ Favorite CRUD ================
def get_favorites_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Favorite]:
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_favorite(db: Session, favorite: FavoriteCreate) -> Favorite:
    db_favorite = Favorite(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def delete_favorite(db: Session, user_id: int, car_id: int) -> bool:
    db_favorite = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.car_id == car_id)
        .first()
    )
    if not db_favorite:
        return False
    db.delete(db_favorite)
    db.commit()
    return True


# ================ Message CRUD ================
def get_messages(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Message]:
    return (
        db.query(Message)
        .filter((Message.sender_id == user_id) | (Message.receiver_id == user_id))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_message(db: Session, message: MessageCreate, sender_id: int) -> Message:
    db_message = Message(**message.dict(), sender_id=sender_id, sent_at=datetime.now())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


# ================ Ad Moderation CRUD ================
def get_moderation_entries(
    db: Session, skip: int = 0, limit: int = 100
) -> List[AdModeration]:
    return db.query(AdModeration).offset(skip).limit(limit).all()


def create_moderation_entry(
    db: Session, moderation: AdModerationCreate
) -> AdModeration:
    db_moderation = AdModeration(**moderation.dict(), moderation_date=datetime.now())
    db.add(db_moderation)
    db.commit()
    db.refresh(db_moderation)
    return db_moderation


def update_moderation_entry(
    db: Session, moderation_id: int, moderation_update: AdModerationUpdate
) -> Optional[AdModeration]:
    db_moderation = (
        db.query(AdModeration).filter(AdModeration.id == moderation_id).first()
    )
    if not db_moderation:
        return None

    update_data = moderation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_moderation, field, value)

    db.commit()
    db.refresh(db_moderation)
    return db_moderation


# ================ Review CRUD ================
def get_reviews_by_car(
    db: Session, car_id: int, skip: int = 0, limit: int = 100
) -> List[Review]:
    return (
        db.query(Review).filter(Review.car_id == car_id).offset(skip).limit(limit).all()
    )


def create_review(db: Session, review: ReviewCreate, user_id: int) -> Review:
    db_review = Review(**review.dict(), user_id=user_id, review_date=datetime.now())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def update_review(
    db: Session, review_id: int, review_update: ReviewUpdate
) -> Optional[Review]:
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        return None

    update_data = review_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)

    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db: Session, review_id: int) -> bool:
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        return False
    db.delete(db_review)
    db.commit()
    return True


# ================ Price History CRUD ================
def get_price_history(
    db: Session, car_id: int, skip: int = 0, limit: int = 100
) -> List[PriceHistory]:
    return (
        db.query(PriceHistory)
        .filter(PriceHistory.car_id == car_id)
        .order_by(PriceHistory.change_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_price_history(db: Session, car_id: int, price: float) -> PriceHistory:
    db_price_history = PriceHistory(
        car_id=car_id, price=price, change_date=datetime.now()
    )
    db.add(db_price_history)
    db.commit()
    db.refresh(db_price_history)
    return db_price_history


# ================ Car Image CRUD ================
def get_car_images(
    db: Session, car_id: int, skip: int = 0, limit: int = 100
) -> List[CarImage]:
    return (
        db.query(CarImage)
        .filter(CarImage.car_id == car_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_car_image(db: Session, car_image: CarImageCreate) -> CarImage:
    db_car_image = CarImage(**car_image.dict())
    db.add(db_car_image)
    db.commit()
    db.refresh(db_car_image)
    return db_car_image


def delete_car_image(db: Session, image_id: int) -> bool:
    db_car_image = db.query(CarImage).filter(CarImage.id == image_id).first()
    if not db_car_image:
        return False
    db.delete(db_car_image)
    db.commit()
    return True
