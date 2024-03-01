from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalchemy_db import get_db_session
from models.auth_orm_models import UsersOrm, RolesOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from schemas import roles


class UsersRepository(SQLAlchemyRepository):
    _model = UsersOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_role_by_user(self, user_role: roles.UserRoleDto) -> str | None:
        self._statement = (
            select(RolesOrm.role_name)
            .join(UsersOrm, UsersOrm.role_id == RolesOrm.id)
            .where(UsersOrm.user_id == user_role.user_id)
        )
        role = await self.read_one()
        return role


def get_users_repository(session: AsyncSession = Depends(get_db_session)):
    return UsersRepository(session=session)
