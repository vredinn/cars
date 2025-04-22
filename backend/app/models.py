from sqlalchemy import (
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
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    avatar_url = Column(Text, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)

    cars = relationship("Car", back_populates="user")
    favorites = relationship("Favorite", backref="user", cascade="all, delete-orphan")
    sent_messages = relationship(
        "Message",
        foreign_keys="[Message.sender_id]",
        backref="sender",
        cascade="all, delete-orphan",
    )
    received_messages = relationship(
        "Message",
        foreign_keys="[Message.receiver_id]",
        backref="receiver",
        cascade="all, delete-orphan",
    )
    saved_searches = relationship(
        "SavedSearch", backref="user", cascade="all, delete-orphan"
    )
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    image_url = Column(Text, nullable=True)
    models = relationship("Model", back_populates="brand")
    cars = relationship("Car", back_populates="brand")


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand_id = Column(
        Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True
    )

    brand = relationship("Brand", back_populates="models")
    cars = relationship("Car", back_populates="model")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    cars = relationship("Car", back_populates="category")


class DriveType(Base):
    __tablename__ = "drive_types"

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True, nullable=False)

    cars = relationship("Car", back_populates="drive_type")


class Transmission(Base):
    __tablename__ = "transmissions"

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True, nullable=False)

    cars = relationship("Car", back_populates="transmission")


class FuelType(Base):
    __tablename__ = "fuel_types"

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True, nullable=False)

    cars = relationship("Car", back_populates="fuel_type")


class SteeringSide(Base):
    __tablename__ = "steering_sides"

    id = Column(Integer, primary_key=True)
    side = Column(String, unique=True, nullable=False)

    cars = relationship("Car", back_populates="steering_side")


class CarCondition(Base):
    __tablename__ = "car_conditions"

    id = Column(Integer, primary_key=True)
    condition = Column(String, unique=True, nullable=False)

    cars = relationship("Car", back_populates="car_condition")


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False, index=True)
    description = Column(Text)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False, index=True)
    drive_type_id = Column(Integer, ForeignKey("drive_types.id"), nullable=False)
    transmission_id = Column(Integer, ForeignKey("transmissions.id"), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey("fuel_types.id"), nullable=False)
    steering_side_id = Column(Integer, ForeignKey("steering_sides.id"), nullable=False)
    car_condition_id = Column(Integer, ForeignKey("car_conditions.id"), nullable=False)
    engine_capacity = Column(Float, nullable=False)
    engine_power = Column(Integer, nullable=False)
    is_sold = Column(Boolean, default=False, index=True)
    mileage = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    listing_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    user = relationship("User", back_populates="cars")
    brand = relationship("Brand", back_populates="cars")
    model = relationship("Model", back_populates="cars")
    category = relationship("Category", back_populates="cars")
    drive_type = relationship("DriveType", back_populates="cars")
    transmission = relationship("Transmission", back_populates="cars")
    fuel_type = relationship("FuelType", back_populates="cars")
    steering_side = relationship("SteeringSide", back_populates="cars")
    car_condition = relationship("CarCondition", back_populates="cars")

    images = relationship(
        "CarImage", back_populates="car", cascade="all, delete-orphan"
    )
    price_history = relationship(
        "PriceHistory", back_populates="car", cascade="all, delete-orphan"
    )
    reviews = relationship("Review", back_populates="car", cascade="all, delete-orphan")
    favorites = relationship("Favorite", backref="car", cascade="all, delete-orphan")
    messages = relationship("Message", backref="car", cascade="all, delete-orphan")
    moderation = relationship(
        "AdModeration", backref="car", uselist=False, cascade="all, delete-orphan"
    )


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="uq_user_car"),)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    receiver_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    message_text = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)


class AdModeration(Base):
    __tablename__ = "ad_moderation"

    id = Column(Integer, primary_key=True)
    car_id = Column(
        Integer, ForeignKey("cars.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    status = Column(String, nullable=False)
    moderator_comment = Column(Text)
    moderation_date = Column(DateTime, default=datetime.utcnow)


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    search_criteria = Column(JSON, nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    review_text = Column(Text)
    rating = Column(Integer)
    review_date = Column(DateTime, default=datetime.utcnow)

    car = relationship("Car", back_populates="reviews")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    change_date = Column(DateTime, default=datetime.utcnow)

    car = relationship("Car", back_populates="price_history")


class CarImage(Base):
    __tablename__ = "car_images"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text, nullable=False)

    car = relationship("Car", back_populates="images")
