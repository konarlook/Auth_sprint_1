from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalchemy_db import get_db_session
from repositories.roles_repository import RolesRepository
from schemas.roles import RolesActionsSchema


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.roles_repo: RolesRepository = RolesRepository(self.session)

    async def get_all_roles(self) -> list[RolesActionsSchema]:
        return await self.roles_repo.get_roles()

    async def delete_role(self, name: str):
        role_data = await self.roles_repo.get_role_by_name(name=name)
        if not role_data:
            return None
        await self.roles_repo.delete(self.roles_repo._model.id, role_data.id)
        return True


@lru_cache()
def get_role_service(
    session: AsyncSession = Depends(get_db_session),
) -> RoleService:
    return RoleService(session)
