import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalchemy_db import get_db_session
from models.auth_orm_models import UsersOrm, RolesOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from schemas.roles import UsersRolesSchema


class UsersRepository(SQLAlchemyRepository):
    _model = UsersOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def verify_role(self, user_id: uuid.UUID) -> UsersRolesSchema | None:
        self._statement = (
            select(RolesOrm.role_name)
            .join(UsersOrm, UsersOrm.role_id == RolesOrm.id)
            .where(UsersOrm.user_id == user_id)
        )
        result = await self.read_one()
        return result

    async def set_role(self, user_id: uuid.UUID, role_id: int):
        await self.merge(
            update_data={"user_id": user_id, "role_id": role_id},
        )
        return True


def get_users_repository(session: AsyncSession = Depends(get_db_session)):
    return UsersRepository(session=session)
