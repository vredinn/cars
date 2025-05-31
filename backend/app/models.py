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
    rating = Column(Float, CheckConstraint("rating >= 0 AND rating <= 5"), nullable=False, default=0)

    cars = relationship("Car", back_populates="user", cascade="all, delete")
    favorites = relationship("Favorite", backref="user", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="[Message.sender_uuid]", back_populates="sender", cascade="all, delete-orphan")
    received_messages = relationship("Message", foreign_keys="[Message.receiver_uuid]", back_populates="receiver", cascade="all, delete-orphan")
    reviews_given = relationship("Review", foreign_keys="[Review.user_uuid]", back_populates="reviewer", cascade="all, delete-orphan")
    reviews_received = relationship("Review", foreign_keys="[Review.seller_uuid]", back_populates="seller", cascade="all, delete-orphan")

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
    favorites = relationship("Favorite", backref="car", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="car", cascade="all, delete-orphan")
    moderation = relationship("AdModeration", backref="car", uselist=False, cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="car", cascade="all, delete-orphan")

    @property
    def user_uuid(self):
        return self.user.uuid if self.user else None

    @property
    def preview_image_url(self):
        return self.images[0].image_url if self.images else None
    
    @property
    def brand_name(self):
        return self.brand.name if self.brand else None
    @property
    def model_name(self):
        return self.model.name if self.model else None

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="uq_user_car"),)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, default=uuid.uuid4)
    car_uuid = Column(UUID, ForeignKey("cars.uuid", ondelete="CASCADE"), nullable=False)
    sender_uuid = Column(UUID, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    receiver_uuid = Column(UUID, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)
    message_text = Column(Text, nullable=False)
    sent_at = Column(DateTime, server_default=func.now(), nullable=False)

    
    sender = relationship("User", foreign_keys=[sender_uuid], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_uuid], back_populates="received_messages")
    car = relationship("Car", foreign_keys=[car_uuid], back_populates="messages")
    

class AdModeration(Base):
    __tablename__ = "ad_moderation"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), unique=True, nullable=False)
    status = Column(String, nullable=False)
    moderator_comment = Column(Text)
    moderation_date = Column(DateTime, server_default=func.now())

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, default=uuid.uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)  # Кто оставил отзыв
    seller_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False)  # О ком отзыв
    deal_uuid = Column(UUID(as_uuid=True), ForeignKey("deals.uuid", ondelete="CASCADE"), nullable=False)
    review_text = Column(Text, nullable=False)
    rating = Column(Float, CheckConstraint("rating >= 1 AND rating <= 5"), nullable=False)
    review_date = Column(DateTime, server_default=func.now())

    deal = relationship("Deal", back_populates="review")
    reviewer = relationship("User", foreign_keys=[user_uuid], back_populates="reviews_given")
    seller = relationship("User", foreign_keys=[seller_uuid], back_populates="reviews_received")

    __table_args__ = (
        # Один отзыв на сделку
        UniqueConstraint("deal_uuid", name="uq_deal_uuid_review"),
    )

    @property
    def user_name(self):
        return self.reviewer.name if self.reviewer else None

    @property
    def user_avatar_url(self):
        return self.reviewer.avatar_url if self.reviewer else None

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

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True, default=uuid.uuid4)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    car = relationship("Car", back_populates="deals")
    seller = relationship("User", foreign_keys=[seller_id], backref="sales")
    buyer = relationship("User", foreign_keys=[buyer_id], backref="purchases")
    review = relationship("Review", back_populates="deal", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        # Проверка что продавец и покупатель разные пользователи
        CheckConstraint("seller_id != buyer_id", name="check_different_users"),
    )

    @property
    def seller_uuid(self):
        return self.seller.uuid if self.seller else None

    @property
    def buyer_uuid(self):
        return self.buyer.uuid if self.buyer else None

    @property
    def car_uuid(self):
        return self.car.uuid if self.car else None
