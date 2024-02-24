from abc import ABC, abstractmethod
from uuid import UUID


class BaseService(ABC):
    def __init__(self, client):
        self.client = client

    async def _create_token(self, user_id: UUID, fresh: bool = False) -> dict[str, str]:
        """Create a new access anda refresh tokens."""
        pass
