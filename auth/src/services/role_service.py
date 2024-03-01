from fastapi import Depends

from repositories.users_repository import UsersRepository, get_users_repository
from schemas import roles
from services.base_service import BaseService


class AuthRoleService(BaseService):
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    async def create(self, role: roles.RoleAction):
        """Create a new role."""
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def verify(self, user_role: roles.UserRoleDto) -> bool:
        db_role = await self.users_repo.get_role_by_user(user_role=user_role)
        is_verify = False
        if db_role == user_role.role_name:
            is_verify = True
        return is_verify


def get_role_service(
    users_repo: UsersRepository = Depends(get_users_repository),
) -> AuthRoleService:
    return AuthRoleService(users_repo=users_repo)
