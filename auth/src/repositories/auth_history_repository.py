import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy_repository import SQLAlchemyRepository
from models.auth_orm_models import AuthHistotyOrm
from schemas.user_model import AuthHistorySchema


class AuthHistoryRepository(SQLAlchemyRepository):
    _model = AuthHistotyOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_auth_history(self, user_id: int):
        self._statement = (
            select(self._model)
            .where(self._model.user_id == user_id)
            .order_by(self._model.dt_login.desc())
        )
        return await self.read()

    async def add_login_history(self, user_id: uuid.UUID):
        auth_history = AuthHistorySchema(
            user_id=user_id,
            id=uuid.uuid4(),
            dt_login=datetime.datetime.now(),
            dt_logout=None,
            device_id=None,
        )
        db_obj = await self.create(auth_history)
        return db_obj

    async def add_logout_history(self, session_id: uuid.UUID):
        now = datetime.datetime.now()
        await self.update(self._model.id, session_id, {"dt_logout": now})
