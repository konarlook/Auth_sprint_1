from services.base_service import BaseService


class AuthRoleService(BaseService):
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError


def get_role_service() -> AuthRoleService:
    return AuthRoleService()
