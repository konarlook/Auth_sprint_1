from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class _BaseService(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError


class BaseService(ABC):
    def __init__(self, client):
        self.client = client

    async def _create_token(self, user_id: UUID, fresh: bool = False) -> dict[str, str]:
        """Create a new access anda refresh tokens."""
        pass

    async def create(self, session: AsyncSession):
        pass

