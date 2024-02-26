from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.auth_orm_models import UserDataOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from schemas.users import FullUserSchema


class UserDataRepository(SQLAlchemyRepository):
    _model = UserDataOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_user_by_email(self, email: str) -> FullUserSchema | None:
        self._statement = select(self._model).where(self._model.email == email)
        raw_result = await self.read_one()
        try:
            result = self.to_pydantic(db_obj=raw_result, pydantic_model=FullUserSchema)
        except TypeError:
            result = None
        return result
