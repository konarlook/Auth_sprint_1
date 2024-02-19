import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class _BaseSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class CommonSettings(_BaseSettings):
    service_name: str = Field(
        default='auth',
        description='Название сервиса авторизации',
    )
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description='Корень проекта',
    )


class PostgresSettings(_BaseSettings):
    postgres_host: str = Field(
        default='postgres_auth',
        description='Адрес хоста Postgres для модуля авторизации',
    )
    postgres_port: int = Field(
        default=5432,
        description='Порт Postgres для сервиса авторизации',
    )
    postgres_database: str = Field(
        default='auth',
        description='База данных для хранения информации пользователей',
    )


class RedisSettings(_BaseSettings):
    redis_host: str = Field(
        default='redis_auth',
        description='Адрес хоста Redis для модуля авторизации',
    )
    redis_port: int = Field(
        default=6379,
        description='Порт Redis для сервиса авторизации',
    )
    redis_database: str = Field(
        default='0',
        description='База данных для хранения токенов',
    )
    redis_time: int = Field(
        default=3600,
        description='Время хранения токенов',
    )


class BackendSettings(_BaseSettings):
    backend_host: str = Field(
        default='auth',
        description="Адрес хоста сервиса авторизации",
    )
    backend_port: int = Field(
        default=8000,
        description="Порт сервиса авторизации",
    )


class Settings(CommonSettings):
    backend: BackendSettings = BackendSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
