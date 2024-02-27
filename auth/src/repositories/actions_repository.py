from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy_repository import SQLAlchemyRepository
from models.auth_orm_models import ActionsOrm


class ActionsRepository(SQLAlchemyRepository):
    _model = ActionsOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_actions_by_names(self, action_names: list[str]):
        self._statement = select(self._model).where(
            self._model.action_name.in_(action_names)
        )
        result = await self.read()
        return result
