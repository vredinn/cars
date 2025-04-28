import uuid
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker

from config import settings
from database import Base
from models import (
    Brand, CarModel, User, Car, CarImage, PriceHistory, Review,
    Favorite, Message, SavedSearch, AdModeration,
    BodyTypeEnum, DriveTypeEnum, TransmissionEnum, FuelTypeEnum,
    SteeringSideEnum, CarConditionEnum
)
from passlib.context import CryptContext

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)
faker = Faker("ru_RU")

def seed_data(session: Session):
    # if session.query(User).first():
    #     print("Seed already applied.")
    #     return

    
    print("⚠ Очистка таблиц...")
    session.query(CarImage).delete()
    session.query(PriceHistory).delete()
    session.query(Message).delete()
    session.query(Favorite).delete()
    session.query(Review).delete()
    session.query(AdModeration).delete()
    session.query(Car).delete()
    session.query(CarModel).delete()
    session.query(Brand).delete()
    session.query(SavedSearch).delete()
    session.query(User).delete()
    session.commit()
    print("✅ Очистка завершена, создаём новые данные...")

    # Users
    users = [
        User(name="Админ", email="admin@example.com", phone="+79990001122",
            password=pwd_context.hash("admin123" + settings.SALT), is_admin=True),
        User(name="Обычный", email="user@example.com", phone="+79998887766",
            password=pwd_context.hash("user123" + settings.SALT))
    ]
    # Добавим ещё пользователей
    for i in range(3):
        users.append(User(
            name=faker.name(),
            email=faker.email(),
            phone=faker.phone_number(),
            password=pwd_context.hash("pass" + settings.SALT)
        ))
    session.add_all(users)

    toyota = Brand(name="Mercedes-Benz", image_url="brand_logos/mercedes.png")
    bmw = Brand(name="BMW", image_url="brand_logos/bmw.png")
    audi = Brand(name="Audi", image_url="brand_logos/audi.png")
    volkswagen = Brand(name="Volkswagen", image_url="brand_logos/volkswagen.png")
    ford = Brand(name="Ford", image_url="brand_logos/frod.png")
    peugeot = Brand(name="Peugeot", image_url="brand_logos/peugeot.png")
    session.add_all([toyota, bmw, audi, volkswagen, ford, peugeot])

    camry = CarModel(name="Camry", brand=toyota)
    corolla = CarModel(name="Corolla", brand=toyota)
    x5 = CarModel(name="X5", brand=bmw)
    a4 = CarModel(name="A4", brand=audi)
    session.add_all([camry, corolla, x5, a4])

    session.flush()  # Чтобы у всех моделей и пользователей были ID

    models = [camry, corolla, x5, a4]
    brands = [toyota, bmw, audi]

    # Cars + Related
    for i in range(10):
        user = random.choice(users)
        model = random.choice(models)
        car = Car(
            uuid=uuid.uuid4(),
            year=random.randint(2005, 2024),
            price=random.randint(500_000, 5_000_000),
            description=faker.text(120),
            user=user,
            body_type=random.choice(list(BodyTypeEnum)),
            brand=model.brand,
            model=model,
            drive_type=random.choice(list(DriveTypeEnum)),
            transmission=random.choice(list(TransmissionEnum)),
            fuel_type=random.choice(list(FuelTypeEnum)),
            steering_side=random.choice(list(SteeringSideEnum)),
            car_condition=random.choice(list(CarConditionEnum)),
            engine_capacity=round(random.uniform(1.3, 4.0), 1),
            engine_power=random.randint(80, 400),
            is_sold=random.choice([False, False, True]),
            mileage=random.randint(0, 300_000),
            color=faker.color_name(),
            listing_date=datetime.now(),
            latitude=faker.latitude(),
            longitude=faker.longitude()
        )
        session.add(car)
        session.flush()

        session.add(PriceHistory(car=car, price=car.price, change_date=datetime.now()))
        session.add(CarImage(car=car, image_url="uploads/example.jpg"))
        session.add(Review(user=random.choice(users), car=car, rating=random.uniform(3.0, 5.0), review_text=faker.sentence(), review_date=datetime.now()))
        session.add(AdModeration(car=car, status="approved", moderator_comment="OK"))

        # Favorite и Message
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u != sender])
        session.add(Favorite(user=sender, car=car))
        session.add(Message(sender_id=sender.id, receiver_id=receiver.id, car=car, message_text=faker.sentence(), sent_at=datetime.now()))

    # Saved Search
    for u in users:
        session.add(SavedSearch(user=u, search_criteria={"q" : f"{random.choice(['Toyota', 'BMW'])} до 3 млн"}))

    session.commit()

if __name__ == "__main__":
    with Session(engine) as session:
        seed_data(session)
