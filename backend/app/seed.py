# seed.py
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database import Base
from models import *
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # берём из .env

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)


def seed_data(session: Session):
    # Проверка, чтобы не дублировать
    if session.query(Brand).first():
        print("База уже содержит данные. Пропускаем посев.")
        return False

    # Примерные данные
    brands = [
        Brand(name="Toyota"),
        Brand(name="BMW"),
        Brand(name="Mercedes"),
        Brand(name="Audi"),
        Brand(name="Volkswagen"),
        Brand(name="Ford"),
        Brand(name="Honda"),
        Brand(name="Hyundai"),
        Brand(name="Kia"),
        Brand(name="Nissan"),
        Brand(name="Jeep"),
        Brand(name="Subaru"),
        Brand(name="Mazda"),
        Brand(name="Lexus"),
        Brand(name="Mitsubishi"),
        Brand(name="Infiniti"),
        Brand(name="Tesla"),
        Brand(name="Porsche"),
        Brand(name="Lamborghini"),
        Brand(name="Ferrari"),
        Brand(name="McLaren"),
        Brand(name="Bugatti"),
        Brand(name="Rolls-Royce"),
        Brand(name="Bentley"),
        Brand(name="Jaguar"),
        Brand(name="Volvo"),
    ]
    session.add_all(brands)

    models = [
        Model(name="Camry", brand=brands[0]),
        Model(name="Corolla", brand=brands[0]),
        Model(name="X5", brand=brands[1]),
        Model(name="E-Class", brand=brands[2]),
        Model(name="A4", brand=brands[3]),
        Model(name="Golf", brand=brands[4]),
        Model(name="Focus", brand=brands[5]),
        Model(name="Civic", brand=brands[6]),
        Model(name="Elantra", brand=brands[7]),
        Model(name="Sportage", brand=brands[8]),
        Model(name="Qashqai", brand=brands[9]),
        Model(name="Wrangler", brand=brands[10]),
        Model(name="Forester", brand=brands[11]),
        Model(name="CX-5", brand=brands[12]),
    ]
    session.add_all(models)

    categories = [
        Category(name="Седан"),
        Category(name="Внедорожник"),
        Category(name="Хэтчбек"),
        Category(name="Купе"),
        Category(name="Универсал"),
        Category(name="Пикап"),
        Category(name="Кабриолет"),
        Category(name="Спорткар"),
        Category(name="Микроавтобус"),
    ]
    drive_types = [
        DriveType(type="Передний"),
        DriveType(type="Полный"),
        DriveType(type="Задний"),
    ]
    transmissions = [
        Transmission(type="Автомат"),
        Transmission(type="Механика"),
        Transmission(type="Робот"),
    ]
    fuel_types = [
        FuelType(type="Бензин"),
        FuelType(type="Дизель"),
        FuelType(type="Электрический"),
        FuelType(type="Гибрид"),
        FuelType(type="Газ"),
    ]
    steering_sides = [SteeringSide(side="Левый"), SteeringSide(side="Правый")]
    car_conditions = [
        CarCondition(condition="Новый"),
        CarCondition(condition="Б/У"),
        CarCondition(condition="Ремонт"),
    ]

    session.add_all(
        categories
        + drive_types
        + transmissions
        + fuel_types
        + steering_sides
        + car_conditions
    )

    users = [
        User(
            name="Иван Иванов",
            email="ivan@example.com",
            password="password",
            phone="1234567890",
            registration_date=datetime.utcnow(),
            is_admin=False,
        ),
        User(
            name="Петр Петров",
            email="petr@example.com",
            password="password",
            phone="9876543210",
            registration_date=datetime.utcnow(),
            is_admin=True,
        ),
    ]
    session.add_all(users)
    session.commit()
    print("Посев данных завершён.")


if __name__ == "__main__":
    with Session(engine) as session:
        seed_data(session)
