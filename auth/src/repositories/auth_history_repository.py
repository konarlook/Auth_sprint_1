import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from repositories.sqlalchemy_repository import SQLAlchemyRepository
from models.auth_orm_models import AuthHistotyOrm
from schemas.histories import FullIdHistorySchema, FullHistorySchema
from db.sqlalchemy_db import get_db_session


class AuthHistoryRepository(SQLAlchemyRepository):
    _model = AuthHistotyOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_auth_history(self, user_id: str) -> list[FullHistorySchema]:
        self._statement = (
            select(self._model)
            .where(self._model.user_id == user_id)
            .order_by(self._model.dt_login.desc())
        )
        raw_result = await self.read()
        result = [
            self.to_pydantic(db_obj=row, pydantic_model=FullHistorySchema)
            for row in raw_result
        ]
        return result

    async def add_login_history(self, user_id: uuid.UUID, device_id: str):
        session = uuid.uuid4()
        auth_history = FullIdHistorySchema(
            id=session,
            user_id=user_id,
            dt_login=datetime.datetime.now(),
            dt_logout=None,
            device_id=device_id,
        )
        await self.create(auth_history.dict())
        return session

    async def add_logout_history(self, session_id: uuid.UUID):
        update_data = {"dt_logout": datetime.datetime.now()}
        await self.update(
            orm_field=self._model.id, where_cond=session_id, update_data=update_data
        )


def get_db_history_client(session: AsyncSession = Depends(get_db_session)):
    return AuthHistoryRepository(session=session)
