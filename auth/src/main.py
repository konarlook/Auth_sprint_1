import logging
from contextlib import asynccontextmanager

import redis
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from core.config import settings
from core.logger import LOGGING

load_dotenv()


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Lifespan for startup and shutdown Redis"""
    _redis = Redis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        db=settings.redis.redis_database,
    )
    yield
    await _redis.close()


app = FastAPI(
    title=settings.service_name,
    description="Сервис авторизации",
    docs_url="/api/description",
    default_response_class=ORJSONResponse,
    version="1.0.0",
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.backend.backend_host,
        port=settings.backend.backend_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )