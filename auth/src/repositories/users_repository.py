from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalchemy_db import get_db_session
from helpers.exceptions import AuthRoleIsNotExistException
from models.auth_orm_models import UsersOrm, RolesOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from schemas import roles


class UsersRepository(SQLAlchemyRepository):
    _model = UsersOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def set_role(self, user_role: roles.UserRoleDto) -> UsersOrm | None:
        role = await self.get_role_by_name(user_role=user_role)
        if not role:
            raise AuthRoleIsNotExistException()
        user_role = UsersOrm(user_id=user_role.user_id, role_id=role.id)
        db_obj = await self.merge(
            {
                "user_id": user_role.user_id,
                "role_id": user_role.role_id,
            }
        )
        return db_obj

    async def get_role_by_name(
        self, user_role: roles.UserRoleDto
    ) -> roles.RoleSchema | None:
        self._statement = select(RolesOrm).where(
            RolesOrm.role_name == user_role.role_name
        )
        role_orm = await self.read_one()
        role = self.to_pydantic(role_orm, roles.RoleSchema)
        return role

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
