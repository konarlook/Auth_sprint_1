import logging
import json
from redis import Redis
from repositories.base import MixinCreateRepository

logger = logging.getLogger(__name__)


class RedisRepository(MixinCreateRepository):
    redis = Redis | None

    def __init__(self, connection=Redis):
        self.connection = connection

    async def get(self, key: str):
        try:
            data = await self.connection.get(str(key))
        except ConnectionError as e:
            data = None
            logger.error(e)

        if not data:
            return None
        return json.loads(data)

    async def create(self, key: str, value: str):
        try:
            await self.connection.set(str(key), value)
        except ConnectionError as e:
            logger.error(e)
