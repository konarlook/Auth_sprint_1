import uuid

from fastapi import Depends

from schemas.histories import HistoryBase
from repositories.auth_history_repository import (AuthHistoryRepository,
                                                  get_db_history_client)
from .base_service import BaseService


class HistoryService(BaseService):
    def __init__(self, database_client: AuthHistoryRepository):
        self.database_client = database_client

    async def get(self):
        pass

    async def create(self, user_id, device_id) -> None:
        _session = await self.database_client.add_login_history(
            user_id=user_id,
            device_id=device_id,
        )
        return _session

    async def delete(self, *args, **kwargs):
        pass

    async def update(self, session_id: uuid.UUID):
        await self.database_client.add_logout_history(session_id)


def get_history_service(
        database_client: AuthHistoryRepository = Depends(get_db_history_client)
) -> HistoryService:
    return HistoryService(database_client=database_client)