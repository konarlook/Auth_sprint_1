import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from .logger import LOGGING

logging_config.dictConfig(LOGGING)
DEBUG = True


class _BaseSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class CommonSettings(_BaseSettings):
    service_name: str = Field(
        default='auth',
        description='Название сервиса авторизации',
    ) if not DEBUG else '0.0.0.0'
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description='Корень проекта',
    )
    debug_mode: bool = Field(
        default=False,
        description="Режим отладки сервиса авторизации",
    )


class PostgresSettings(_BaseSettings):
    postgres_host: str = Field(
        default='postgres_auth',
        description='Адрес хоста Postgres для модуля авторизации',
    ) if not DEBUG else '0.0.0.0'
    postgres_port: int = Field(
        default=5432,
        description='Порт Postgres для сервиса авторизации',
    )
    postgres_database: str = Field(
        default='auth',
        description='База данных для хранения информации пользователей',
    )
    postgres_user: str = Field(default='auth_user')
    postgres_password: str = Field(default='auth_pass')

    @property
    def database_url_asyncpg(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_database,
        )


class RedisSettings(_BaseSettings):
    auth_redis_host: str = Field(
        default='redis_auth',
        description='Адрес хоста Redis для модуля авторизации',
    ) if not DEBUG else '0.0.0.0'
    auth_redis_port: int = Field(
        default=6379,
        description='Порт Redis для сервиса авторизации',
    )
    auth_redis_database: str = Field(
        default='0',
        description='База данных для хранения токенов',
    )
    auth_redis_password: str = Field(
        default='auth_pass',
        description='Пароль от Redis',
    )
    auth_redis_time: int = Field(
        default=3600,
        description='Время хранения токенов',
    )


class BackendSettings(_BaseSettings):
    auth_backend_host: str = Field(
        default='auth',
        description="Адрес хоста сервиса авторизации",
    ) if not DEBUG else '0.0.0.0'
    auth_backend_port: int = Field(
        default=8000,
        description="Порт сервиса авторизации",
    )
    auth_secret_key: str = Field(
        default='123qwerty',
        description='Секретный ключ для генерации токенов',
    )
    auth_refresh_token_lifetime: int = Field(
        default='1'
    )
    auth_algorithm_password: str = Field(
        default='HS256',
        description='Алгоритм шифрования токена',
    )


class Settings(CommonSettings):
    backend: BackendSettings = BackendSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
