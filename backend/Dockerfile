# auto-listings/backend/Dockerfile
FROM python:3.13-slim-bookworm

# Устанавливаем git и сборочные утилиты
RUN apt-get update && \
    apt-get install -y git build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение и переходим в каталог с main.py
COPY ./app ./app
WORKDIR /app/app

EXPOSE 8000
# Запуск FastAPI CLI в режиме разработки (с авто‑перезагрузкой при изменениях)
CMD ["fastapi", "dev", "main.py"]
