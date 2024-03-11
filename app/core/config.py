import os
from logging import config as logging_config

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class DBParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_", env_file=".env")

    host: str
    port: int
    db: str
    user: str
    password: str

    def url(self):
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class ElasticParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTIC_", env_file=".env")

    host: str
    port: int

    def url(self):
        return f"http://{self.host}:{self.port}"


class RedisParams(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=".env")

    host: str
    port: int

    def url(self):
        return f"{self.host}:{self.port}"


# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
