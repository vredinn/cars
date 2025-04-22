-- Справочные справочники
CREATE TABLE IF NOT EXISTS brands (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    brand_id INTEGER NOT NULL REFERENCES brands(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS drive_types (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS transmissions (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS fuel_types (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS steering_sides (
    id SERIAL PRIMARY KEY,
    side TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS car_conditions (
    id SERIAL PRIMARY KEY,
    condition TEXT NOT NULL UNIQUE
);

-- Основные сущности
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone TEXT,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    year VARCHAR(4) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    brand_id INTEGER NOT NULL REFERENCES brands(id),
    model_id INTEGER NOT NULL REFERENCES models(id),
    drive_type_id INTEGER NOT NULL REFERENCES drive_types(id),
    transmission_id INTEGER NOT NULL REFERENCES transmissions(id),
    fuel_type_id INTEGER NOT NULL REFERENCES fuel_types(id),
    steering_side_id INTEGER NOT NULL REFERENCES steering_sides(id),
    car_condition_id INTEGER NOT NULL REFERENCES car_conditions(id),
    engine_capacity INTEGER,
    engine_power INTEGER,
    car_address TEXT,
    is_sold BOOLEAN NOT NULL DEFAULT FALSE,
    mileage INTEGER,
    listing_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- Вспомогательные сущности
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    UNIQUE (user_id, car_id)
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ad_moderation (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    status TEXT NOT NULL,
    moderator_comment TEXT,
    moderation_date TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS saved_searches (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    search_criteria JSONB NOT NULL,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    review_text TEXT,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    review_date TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    price NUMERIC(12,2) NOT NULL,
    change_date TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS car_images (
    id SERIAL PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL
);

-- Индексы для ускорения поиска по FK‑полям
CREATE INDEX IF NOT EXISTS idx_cars_user ON cars(user_id);
CREATE INDEX IF NOT EXISTS idx_cars_brand ON cars(brand_id);
CREATE INDEX IF NOT EXISTS idx_cars_model ON cars(model_id);
CREATE INDEX IF NOT EXISTS idx_messages_car ON messages(car_id);
CREATE INDEX IF NOT EXISTS idx_reviews_car ON reviews(car_id);
CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_price_history_car ON price_history(car_id);
