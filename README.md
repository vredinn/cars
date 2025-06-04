# Маркетплейс автомобилей

Проект состоит из бэкенда на FastAPI, базы данных PostgreSQL и фронтенда на Vue.js.

## Предварительные требования

- Docker
- Docker Compose

## Начало работы

### Запуск с помощью Docker

1. Запустите все сервисы с помощью Docker Compose:
```bash
docker-compose up -d --build
```

Это запустит три контейнера:
- Фронтенд (Vue.js)
- Бэкенд (FastAPI)
- База данных (PostgreSQL)

### Миграции базы данных

Для работы с миграциями базы данных выполните следующие команды в контейнере бэкенда:

1. Создание новой миграции:
```bash
docker-compose exec backend alembic revision --autogenerate -m "название_миграции"
```

2. Применение миграций:
```bash
docker-compose exec backend alembic upgrade head
```

### Заполнение начальными данными

Для заполнения базы данных начальными данными выполните:

```bash
docker-compose exec backend python app/seed.py
```

Примечание: Все начальные пользователи, созданные скриптом seed.py, имеют следующие учетные данные:
- Пароль: `Password123`

## Доступ к приложению

- Фронтенд: http://localhost:3000
- API бэкенда: http://localhost:8000
- Документация API: http://localhost:8000/docs

### Структура проекта

```
.
├── frontend/          # Фронтенд приложение на Vue.js
├── backend/           # Бэкенд приложение на FastAPI
└── db/               # Директория с данными PostgreSQL
```

### Полезные команды Docker

- Просмотр логов:
```bash
docker-compose logs -f
```

- Перезапуск сервисов:
```bash
docker-compose restart
```

- Остановка всех сервисов:
```bash
docker-compose down
```

- Пересборка и запуск сервисов:
```bash
docker-compose up -d --build
```
