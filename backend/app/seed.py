import uuid
import random
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from faker import Faker

from config import settings
from database import Base
from models import (
    Brand, CarModel, User, Car, PriceHistory, Review,
    Favorite, Message, AdModeration, Deal, CarImage,
    BodyTypeEnum, DriveTypeEnum, TransmissionEnum, FuelTypeEnum,
    SteeringSideEnum, CarConditionEnum
)
from passlib.context import CryptContext

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)
faker = Faker("ru_RU")

def update_user_rating(session: Session, user_uuid: uuid.UUID):
    reviews = session.query(Review).filter(Review.seller_uuid == user_uuid).all()
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
        user = session.query(User).filter(User.uuid == user_uuid).first()
        if user:
            user.rating = round(avg_rating, 1)

def seed_data(session: Session):
    print("Очистка таблиц...")
    session.query(PriceHistory).delete()
    session.query(Message).delete()
    session.query(Favorite).delete()
    session.query(Review).delete()
    session.query(AdModeration).delete()
    session.query(Deal).delete()
    session.query(CarImage).delete()
    session.query(Car).delete()
    session.query(CarModel).delete()
    session.query(Brand).delete()
    session.query(User).delete()
    session.commit()
    print("Очистка завершена, создание новых данных...")

    admin_user = User(
        uuid=uuid.uuid4(),
        name="Админ",
        email="admin@example.com",
        phone="+79990001122",
        password=pwd_context.hash("Password123" + settings.SALT),
        is_admin=True,
        rating=0,
        registration_date=datetime.now()
    )
    
    regular_users = [
        User(
            uuid=uuid.uuid4(),
            name="Обычный",
            email="user@example.com",
            phone="+79998887766",
            password=pwd_context.hash("Password123" + settings.SALT),
            rating=0,
            registration_date=datetime.now()
        )
    ]
    
    for i in range(8):
        regular_users.append(User(
            uuid=uuid.uuid4(),
            name=faker.name(),
            email=faker.unique.email(),
            phone=faker.phone_number(),
            password=pwd_context.hash("Password123" + settings.SALT),
            rating=0,
            registration_date=datetime.now(),
        ))
    
    session.add(admin_user)
    session.add_all(regular_users)
    session.flush()

    toyota = Brand(name="Toyota", image_url="/brand_logos/toyota.png")
    bmw = Brand(name="BMW", image_url="/brand_logos/bmw.png")
    audi = Brand(name="Audi", image_url="/brand_logos/audi.png")
    volkswagen = Brand(name="Volkswagen", image_url="/brand_logos/volkswagen.png")
    ford = Brand(name="Ford", image_url="/brand_logos/ford.png")
    peugeot = Brand(name="Peugeot", image_url="/brand_logos/peugeot.png")
    mercedes = Brand(name="Mercedes-Benz", image_url="/brand_logos/mercedes.png")
    brands = [toyota, bmw, audi, volkswagen, ford, peugeot, mercedes]
    session.add_all(brands)
    session.flush()

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

    cars = []
    for i in range(50):
        user = random.choice(regular_users)
        model = random.choice(models)
        price = Decimal(str(random.randint(500_000, 10_000_000)))
        is_sold = random.choice([False, False, False, True])

        car = Car(
            uuid=uuid.uuid4(),
            year=random.randint(2005, 2025),
            price=price,
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
            is_sold=is_sold,
            mileage=random.randint(0, 400_000),
            color=faker.color_name(),
            listing_date=datetime.now(),
            latitude=Decimal(str(faker.latitude())),
            longitude=Decimal(str(faker.longitude()))
        )
        cars.append(car)
        session.add(car)
        session.flush()

        session.add(PriceHistory(
            car_id=car.id,
            price=price,
            change_date=datetime.now()
        ))

        if is_sold:
            status = "approved"
        else:
            status = random.choice(["approved", "pending", "rejected"])

        session.add(AdModeration(
            car_id=car.id,
            status=status,
            moderator_comment=faker.sentence() if status != "approved" else None,
            moderation_date=datetime.now(),
            moderator_id=admin_user.id if status != "pending" else None
        ))

        # Favorites
        if random.choice([True, False]):
            potential_users = [u for u in regular_users if u.id != car.user_id]
            if potential_users:
                session.add(Favorite(
                    user_id=random.choice(potential_users).id,
                    car_id=car.id
                ))

    for car in cars:
        if car.is_sold:
            buyer = random.choice([u for u in regular_users if u.id != car.user_id])
            deal = Deal(
                uuid=uuid.uuid4(),
                car_id=car.id,
                seller_id=car.user_id,
                buyer_id=buyer.id,
                created_at=datetime.now(),
            )
            session.add(deal)
            session.flush()

            review = Review(
                uuid=uuid.uuid4(),
                user_uuid=buyer.uuid,
                seller_uuid=car.user.uuid,  # seller
                deal_uuid=deal.uuid,
                rating=random.randint(3, 5),
                review_text=faker.paragraph(nb_sentences=2),
                review_date=datetime.now()
            )
            session.add(review)
            session.flush()
            update_user_rating(session, car.user.uuid)

    for _ in range(30):
        car = random.choice(cars)
        sender = random.choice(regular_users)
        receiver = car.user if sender != car.user else random.choice([u for u in regular_users if u != sender])
        session.add(Message(
            uuid=uuid.uuid4(),
            car_uuid=car.uuid,
            sender_uuid=sender.uuid,
            receiver_uuid=receiver.uuid,
            message_text=faker.paragraph(nb_sentences=1),
            sent_at=datetime.now()
        ))

    session.commit()
    print("Данные успешно созданы")

if __name__ == "__main__":
    with Session(engine) as session:
        seed_data(session)