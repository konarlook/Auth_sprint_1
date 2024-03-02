from redis.asyncio import Redis
from core.config import settings

redis: Redis = Redis(
    host='0.0.0.0',#settings.redis.auth_redis_host,
    port=settings.redis.auth_redis_port,
    db=settings.redis.auth_redis_database,
)


async def get_redis() -> Redis:
    redis_client = redis
    return redis_client
