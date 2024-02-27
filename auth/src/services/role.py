import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.sqlalchemy_db import get_db_session
from repositories.actions_repository import ActionsRepository
from repositories.mixactions_repository import MixActionsRepository
from repositories.roles_repository import RolesRepository
from repositories.users_repository import UsersRepository
from schemas.roles import RolesActionsSchema, CreateRoleSchema, RoleBaseSchema


class RoleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.roles_repo: RolesRepository = RolesRepository(self.session)
        self.users_repo: UsersRepository = UsersRepository(self.session)
        self.actions_repo: ActionsRepository = ActionsRepository(self.session)
        self.mixactions_repo: MixActionsRepository = MixActionsRepository(self.session)

    async def get_all_roles(self) -> list[RolesActionsSchema]:
        return await self.roles_repo.get_roles()

    async def is_exist_role(self, name: str) -> bool:
        role_data = await self.roles_repo.get_role_by_name(name=name)
        if not role_data:
            return None
        return role_data

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

    async def verify_role(self, user_id: uuid.UUID, role_name: str):
        role_name_response = await self.users_repo.verify_role(user_id=user_id)
        is_true = False
        if role_name_response == role_name:
            is_true = True
        return is_true

    async def create_role(self, role_data: CreateRoleSchema):
        role = RoleBaseSchema(role_name=role_data.role_name, comment=role_data.comment)
        await self.roles_repo.create(role)
        action_names = [i[0] for i in role_data.actions if i[-1]]
        response_names = await self.actions_repo.get_actions_by_names(
            action_names=action_names
        )
        roles_ids = [row.id for row in response_names]
        await self.mixactions_repo.set_actions_to_role(
            role_id=role.id, action_ids=roles_ids
        )
        return True


@lru_cache()
def get_role_service(
    session: AsyncSession = Depends(get_db_session),
) -> RoleService:
    return RoleService(session)
