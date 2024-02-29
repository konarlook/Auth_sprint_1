from redis.asyncio import Redis
from core.config import settings


async def get_redis() -> Redis:
    client = Redis(
        host=settings.redis.auth_redis_host,
        port=settings.redis.auth_redis_port,
        db=settings.redis.auth_redis_database,
    )
    return client
