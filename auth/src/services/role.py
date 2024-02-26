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


@lru_cache()
def get_role_service(
    session: AsyncSession = Depends(get_db_session),
) -> RoleService:
    return RoleService(session)
