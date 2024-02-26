import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models.auth_orm_models import UsersOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    _model = UsersOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def assign_role(self, user_id: uuid.UUID, role_id: int):
        ...
