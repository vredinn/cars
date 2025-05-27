import uuid
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker

from config import settings
from database import Base
from models import (
    Brand, CarModel, User, Car, PriceHistory, Review,
    Favorite, Message, AdModeration,
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
    print("⚠ Очистка таблиц...")
    session.query(PriceHistory).delete()
    session.query(Message).delete()
    session.query(Favorite).delete()
    session.query(Review).delete()
    session.query(AdModeration).delete()
    session.query(Car).delete()
    session.query(CarModel).delete()
    session.query(Brand).delete()
    session.query(User).delete()
    session.commit()
    print("✅ Очистка завершена, создаём новые данные...")

    # Users
    users = [
        User(
            name="Админ",
            email="admin@example.com",
            phone="+79990001122",
            password=pwd_context.hash("Password123" + settings.SALT),
            is_admin=True,
            rating=random.uniform(3.0, 5.0),
            registration_date=datetime.now()
        ),
        User(
            name="Обычный",
            email="user@example.com",
            phone="+79998887766",
            password=pwd_context.hash("Password123" + settings.SALT),
            rating=random.uniform(3.0, 5.0),
            registration_date=datetime.now()
        )
    ]
    # Additional users
    for i in range(8):
        users.append(User(
            name=faker.name(),
            email=faker.unique.email(),
            phone=faker.phone_number(),
            password=pwd_context.hash("Password123" + settings.SALT),
            rating=random.uniform(2.0, 5.0),
            registration_date=datetime.now()
        ))
    session.add_all(users)
    session.flush()

    # Brands
    toyota = Brand(name="Toyota", image_url="brand_logos/toyota.png")
    bmw = Brand(name="BMW", image_url="brand_logos/bmw.png")
    audi = Brand(name="Audi", image_url="brand_logos/audi.png")
    volkswagen = Brand(name="Volkswagen", image_url="brand_logos/volkswagen.png")
    ford = Brand(name="Ford", image_url="brand_logos/ford.png")
    peugeot = Brand(name="Peugeot", image_url="brand_logos/peugeot.png")
    mercedes = Brand(name="Mercedes-Benz", image_url="brand_logos/mercedes.png")
    brands = [toyota, bmw, audi, volkswagen, ford, peugeot, mercedes]
    session.add_all(brands)
    session.flush()

    # Car Models
    models = [
        CarModel(name="Camry", brand=toyota),
        CarModel(name="Corolla", brand=toyota),
        CarModel(name="RAV4", brand=toyota),
        CarModel(name="Land Cruiser", brand=toyota),
        CarModel(name="3 Series", brand=bmw),
        CarModel(name="X5", brand=bmw),
        CarModel(name="5 Series", brand=bmw),
        CarModel(name="X3", brand=bmw),
        CarModel(name="A4", brand=audi),
        CarModel(name="Q5", brand=audi),
        CarModel(name="A6", brand=audi),
        CarModel(name="Q7", brand=audi),
        CarModel(name="Passat", brand=volkswagen),
        CarModel(name="Tiguan", brand=volkswagen),
        CarModel(name="Golf", brand=volkswagen),
        CarModel(name="Focus", brand=ford),
        CarModel(name="Mustang", brand=ford),
        CarModel(name="Explorer", brand=ford),
        CarModel(name="308", brand=peugeot),
        CarModel(name="3008", brand=peugeot),
        CarModel(name="C-Class", brand=mercedes),
        CarModel(name="E-Class", brand=mercedes),
        CarModel(name="GLC", brand=mercedes)
    ]
    session.add_all(models)
    session.flush()

    # Cars + Related
    for i in range(20):
        user = random.choice(users)
        model = random.choice(models)
        car = Car(
            uuid=uuid.uuid4(),
            year=random.randint(2000, 2025),
            price=random.randint(500_000, 10_000_000),
            description=faker.text(max_nb_chars=200),
            user_id=user.id,
            body_type=random.choice(list(BodyTypeEnum)),
            brand_id=model.brand.id,
            model_id=model.id,
            drive_type=random.choice(list(DriveTypeEnum)),
            transmission=random.choice(list(TransmissionEnum)),
            fuel_type=random.choice(list(FuelTypeEnum)),
            steering_side=random.choice(list(SteeringSideEnum)),
            car_condition=random.choice(list(CarConditionEnum)),
            engine_capacity=round(random.uniform(1.0, 6.0), 1),
            engine_power=random.randint(70, 500),
            is_sold=random.choice([False, False, True]),
            mileage=random.randint(0, 400_000),
            color=faker.color_name(),
            listing_date=datetime.now(),
            latitude=faker.latitude(),
            longitude=faker.longitude()
        )
        session.add(car)
        session.flush()

        # Price History
        session.add(PriceHistory(car_id=car.id, price=car.price, change_date=datetime.now()))
        # Review
        session.add(Review(
            user_id=random.choice(users).id,
            car_id=car.id,
            rating=random.uniform(2.0, 5.0),
            review_text=faker.paragraph(nb_sentences=2),
            review_date=datetime.now()
        ))
        # Ad Moderation
        session.add(AdModeration(
            car_id=car.id,
            status=random.choice(["approved", "pending", "rejected"]),
            moderator_comment=faker.sentence() if random.choice([True, False]) else None,
            moderation_date=datetime.now()
        ))

        # Favorite and Message
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u != sender])
        session.add(Favorite(user_id=sender.id, car_id=car.id))
        session.add(Message(
            car_uuid=car.uuid,
            sender_uuid=sender.uuid,
            receiver_uuid=receiver.uuid,
            message_text=faker.paragraph(nb_sentences=1),
            sent_at=datetime.now()
        ))

    session.commit()
    print("✅ Данные успешно созданы!")

if __name__ == "__main__":
    with Session(engine) as session:
        seed_data(session)