from redis.asyncio import Redis

from core.config import settings


async def get_redis() -> Redis:
    client = Redis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        db=settings.redis.redis_database,
    )
    return client
