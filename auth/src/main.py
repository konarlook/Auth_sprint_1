import logging
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from core.config import settings
from core.logger import LOGGING
from api.v1 import users, roles

load_dotenv()


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Lifespan for startup and shutdown Redis"""
    _redis = Redis(
        host=settings.redis.auth_redis_host,
        port=settings.redis.auth_redis_port,
        db=settings.redis.auth_redis_database,
    )
    yield
    await _redis.close()


app = FastAPI(
    title=settings.service_name,
    description="Сервис авторизации",
    docs_url="/auth/api/openapi",
    openapi_url="/auth/api/openapi.json",
    default_response_class=ORJSONResponse,
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router=users.router)
app.include_router(router=roles.router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",  # settings.backend.backend_host,
        port=8888,  # settings.backend.backend_port,
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
