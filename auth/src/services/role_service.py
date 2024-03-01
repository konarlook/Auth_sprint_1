from fastapi import Depends

from helpers.exceptions import AuthRoleIsAlreadySetException
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

    async def set_role(self, user_role: roles.UserRoleDto) -> roles.UserRole | None:
        """Set role for user."""
        is_need_update = await self.verify(user_role=user_role)
        if is_need_update:
            raise AuthRoleIsAlreadySetException()
        db_obj = await self.users_repo.set_role(user_role=user_role)
        return db_obj

    async def verify(self, user_role: roles.UserRoleDto) -> bool:
        """Verify role for user."""
        db_role = await self.users_repo.get_role_by_user(user_role=user_role)
        is_verify = False
        if db_role == user_role.role_name:
            is_verify = True
        return is_verify


def get_role_service(
    users_repo: UsersRepository = Depends(get_users_repository),
) -> AuthRoleService:
    return AuthRoleService(users_repo=users_repo)
