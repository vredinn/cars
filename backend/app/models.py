from sqlalchemy import (
    UUID,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Float,
    ForeignKey,
    Numeric,
    JSON,
    DateTime,
    UniqueConstraint,
    CheckConstraint,
    Enum,
    func,
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid
import enum

# Enum-классы
class DriveTypeEnum(str, enum.Enum):
    fwd = "Передний"
    rwd = "Задний"
    awd = "Полный"
    fourwd = "4x4"

class TransmissionEnum(str, enum.Enum):
    manual = "Механика"
    automatic = "Автомат"
    cvt = "Вариатор"
    robot = "Робот"

class FuelTypeEnum(str, enum.Enum):
    petrol = "Бензин"
    diesel = "Дизель"
    electric = "Электро"
    hybrid = "Гибрид"

class SteeringSideEnum(str, enum.Enum):
    left = "Левый"
    right = "Правый"

class CarConditionEnum(str, enum.Enum):
    new = "Новый"
    used = "Б/У"
    after_repair = "После ремонта"
    damaged = "Повреждённый"
    for_parts = "На запчасти"

class BodyTypeEnum(str, enum.Enum):
    sedan = "Седан"
    hatchback = "Хэтчбек"
    liftback = "Лифтбек"
    suv = "Внедорожник"
    crossover = "Кроссовер"
    coupe = "Купе"
    convertible = "Кабриолет"
    wagon = "Универсал"
    minivan = "Минивэн"
    van = "Фургон"
    pickup = "Пикап"
    roadster = "Родстер"
    limousine = "Лимузин"
    targa = "Тарга"
    fastback = "Фастбэк"
    microcar = "Микрокар"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(128), nullable=False, doc="Hashed password")
    phone = Column(String, nullable=False)
    registration_date = Column(DateTime, server_default=func.now(), nullable=False)
    avatar_url = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    cars = relationship("Car", back_populates="user", cascade="all, delete")
    favorites = relationship("Favorite", backref="user", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", backref="sender", cascade="all, delete-orphan")
    received_messages = relationship("Message", foreign_keys="[Message.receiver_id]", backref="receiver", cascade="all, delete-orphan")
    saved_searches = relationship("SavedSearch", backref="user", cascade="all, delete-orphan")
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    image_url = Column(Text, nullable=True)
    models = relationship("CarModel", back_populates="brand", cascade="all, delete")
    cars = relationship("Car", back_populates="brand", cascade="all, delete")

class CarModel(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True)

    brand = relationship("Brand", back_populates="models")
    cars = relationship("Car", back_populates="model")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, default=uuid.uuid4)
    year = Column(Integer, nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False, index=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    body_type = Column(Enum(BodyTypeEnum, name="body_type_enum"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    drive_type = Column(Enum(DriveTypeEnum, name="drive_type_enum"), nullable=False)
    transmission = Column(Enum(TransmissionEnum, name="transmission_enum"), nullable=False)
    fuel_type = Column(Enum(FuelTypeEnum, name="fuel_type_enum"), nullable=False)
    steering_side = Column(Enum(SteeringSideEnum, name="steering_side_enum"), nullable=False)
    car_condition = Column(Enum(CarConditionEnum, name="car_condition_enum"), nullable=False)
    engine_capacity = Column(Float, nullable=False)
    engine_power = Column(Integer, nullable=False)
    is_sold = Column(Boolean, default=False, index=True)
    mileage = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    listing_date = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    latitude = Column(Numeric(8, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)

    user = relationship("User", back_populates="cars")
    brand = relationship("Brand", back_populates="cars")
    model = relationship("CarModel", back_populates="cars")

    images = relationship("CarImage", back_populates="car", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="car", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="car", cascade="all, delete-orphan")
    favorites = relationship("Favorite", backref="car", cascade="all, delete-orphan")
    messages = relationship("Message", backref="car", cascade="all, delete-orphan")
    moderation = relationship("AdModeration", backref="car", uselist=False, cascade="all, delete-orphan")
    @property
    def brand_name(self):
        return self.brand.name if self.brand else ""

    @property
    def model_name(self):
        return self.model.name if self.model else ""

    @property
    def preview_image_url(self):
        return self.images[0].image_url if self.images else None

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="uq_user_car"),)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message_text = Column(Text, nullable=False)
    sent_at = Column(DateTime, server_default=func.now())

class AdModeration(Base):
    __tablename__ = "ad_moderation"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), unique=True, nullable=False)
    status = Column(String, nullable=False)
    moderator_comment = Column(Text)
    moderation_date = Column(DateTime, server_default=func.now())

class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    search_criteria = Column(JSON, nullable=False)
    saved_at = Column(DateTime, server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    review_text = Column(Text)
    rating = Column(Float, CheckConstraint("rating >= 0 AND rating <= 5"))
    review_date = Column(DateTime, server_default=func.now())

    car = relationship("Car", back_populates="reviews")

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="uq_user_car_review"),)

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    change_date = Column(DateTime, server_default=func.now())

    car = relationship("Car", back_populates="price_history")

class CarImage(Base):
    __tablename__ = "car_images"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text, nullable=False)

    car = relationship("Car", back_populates="images")
