import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalchemy_db import get_db_session
from repositories.roles_repository import RolesRepository
from repositories.users_repository import UsersRepository
from schemas.roles import RolesActionsSchema


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.roles_repo: RolesRepository = RolesRepository(self.session)
        self.users_repo: UsersRepository = UsersRepository(self.session)

    async def get_all_roles(self) -> list[RolesActionsSchema]:
        return await self.roles_repo.get_roles()

    async def is_exist_role(self, name: str) -> bool:
        role_data = await self.roles_repo.get_role_by_name(name=name)
        if not role_data:
            return False
        return True

    async def delete_role(self, name: str):
        role_data = await self.is_exist_role(name=name)
        if not role_data:
            return None
        await self.roles_repo.delete(self.roles_repo._model.id, role_data.id)
        return True

    async def set_role(self, user_id: uuid.UUID, role_name: str):
        role_data = await self.roles_repo.get_role_by_name(name=role_name)
        await self.users_repo.set_role(user_id=user_id, role_id=role_data.id)
        return True


@lru_cache()
def get_role_service(
    session: AsyncSession = Depends(get_db_session),
) -> RoleService:
    return RoleService(session)
