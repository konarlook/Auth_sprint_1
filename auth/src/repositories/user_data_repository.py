from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.auth_orm_models import UserDataOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository


class UserDataRepository(SQLAlchemyRepository):
    _model = UserDataOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_user_by_email(self, email: str):
        self._statement = select(self._model).where(self._model.email == email)
        return await self.read()
