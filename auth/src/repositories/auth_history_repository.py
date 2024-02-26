import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy_repository import SQLAlchemyRepository
from models.auth_orm_models import AuthHistotyOrm
from schemas.histories import HistoryBase


class AuthHistoryRepository(SQLAlchemyRepository):
    _model = AuthHistotyOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_auth_history(self, user_id: int) -> list[HistoryBase]:
        self._statement = (
            select(self._model)
            .where(self._model.user_id == user_id)
            .order_by(self._model.dt_login.desc())
        )
        raw_result = await self.read()
        result = [
            self.to_pydantic(db_obj=row, pydantic_model=HistoryBase)
            for row in raw_result
        ]
        return result

    async def add_login_history(self, user_id: uuid.UUID, device_id: str):
        auth_history = HistoryBase(
            id=uuid.uuid4(),
            user_id=user_id,
            dt_login=datetime.datetime.now(),
            dt_logout=None,
            device_id=device_id,
        )
        return await self.create(auth_history)

    async def add_logout_history(self, session_id: uuid.UUID):
        update_data = {"dt_logout": datetime.datetime.now()}
        await self.update(
            orm_field=self._model.id, where_cond=session_id, update_data=update_data
        )
