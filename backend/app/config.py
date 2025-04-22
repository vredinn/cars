from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

# Явная загрузка переменных окружения из .env файла
load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    JWT_SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def JWT_SECRET_KEY(self) -> str:
        return self.JWT_SECRET_KEY

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
