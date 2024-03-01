from fastapi import Depends

from helpers.exceptions import (
    AuthRoleIsAlreadySetException,
    AuthRoleIsNotExistException,
)
from repositories.roles_repository import RolesRepository, get_roles_repository
from repositories.users_repository import UsersRepository, get_users_repository
from schemas import roles
from services.base_service import BaseService


class AuthRoleService(BaseService):
    def __init__(self, users_repo: UsersRepository, roles_repo: RolesRepository):
        self.users_repo = users_repo
        self.roles_repo = roles_repo

    async def create(self, role: roles.RoleAction):
        """Create a new role."""
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, name: str):
        role = await self.roles_repo.get_role_by_name(role_name=name)
        if not role:
            raise AuthRoleIsNotExistException()
        await self.roles_repo.delete(self.roles_repo._model.id, role.id)

    async def set_role(self, user_role: roles.UserRoleDto) -> roles.UserRole | None:
        """Set role for user."""
        is_need_update = await self.verify(user_role=user_role)
        if is_need_update:
            raise AuthRoleIsAlreadySetException()
        role = await self.roles_repo.get_role_by_name(role_name=user_role.role_name)
        if not role:
            raise AuthRoleIsNotExistException()
        db_obj = await self.users_repo.set_role(
            user_id=user_role.user_id, role_id=role.id
        )
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
    roles_repo: RolesRepository = Depends(get_roles_repository),
) -> AuthRoleService:
    return AuthRoleService(users_repo=users_repo, roles_repo=roles_repo)
