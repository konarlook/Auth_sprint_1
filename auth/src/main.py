import logging
from contextlib import asynccontextmanager

import uvicorn
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis

from api.v1 import users, roles
from core.config import settings
from core.logger import LOGGING
from helpers.jager import configure_tracer

load_dotenv(find_dotenv())


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Lifespan for startup and shutdown Redis"""
    configure_tracer(
        settings.jaeger.jaeger_host,
        settings.jaeger.jaeger_port,
        settings.service_name,
    )
    _redis = Redis(
        host=settings.redis.auth_redis_host,
        port=settings.redis.auth_redis_port,
        db=settings.redis.auth_redis_database,
    )
    yield
    await _redis.close()


tracer = trace.get_tracer(__name__)

app = FastAPI(
    title=settings.service_name,
    description="Сервис авторизации",
    docs_url="/auth/api/openapi",
    openapi_url="/auth/api/openapi.json",
    default_response_class=ORJSONResponse,
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def before_request(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id")
    print("request_id", request_id)
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "X-Request-Id is required"},
        )
    with tracer.start_as_current_span("auth_request") as span:
        span.set_attribute("http.request_id", request_id)
        response = await call_next(request)
        return response


FastAPIInstrumentor.instrument_app(app)

app.include_router(router=users.router)
app.include_router(router=roles.router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.backend.auth_backend_host,
        port=settings.backend.auth_backend_port,
        reload=True,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
