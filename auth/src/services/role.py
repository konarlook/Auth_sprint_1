import uuid
from functools import lru_cache

from fastapi import Depends

from repositories.actions_repository import ActionsRepository, get_actions_repository
from repositories.mixactions_repository import (
    MixActionsRepository,
    get_mix_actions_repository,
)
from repositories.roles_repository import RolesRepository, get_roles_repository
from repositories.users_repository import UsersRepository, get_users_repository
from schemas.roles import RolesActionsSchema, CreateRoleSchema, RoleBaseSchema


class RoleService:
    def __init__(
        self,
        roles_repo: RolesRepository,
        users_repo: UsersRepository,
        actions_repo: ActionsRepository,
        mixactions_repo: MixActionsRepository,
    ):
        self.roles_repo = roles_repo
        self.users_repo = users_repo
        self.actions_repo = actions_repo
        self.mixactions_repo = mixactions_repo

    async def get_all_roles(self) -> list[RolesActionsSchema]:
        return await self.roles_repo.get_roles()

    async def get_role_by_name(self, name: str):
        role_data = await self.roles_repo.get_role_by_name(name=name)
        if not role_data:
            return None
        return role_data

    async def delete_role(self, name: str):
        role_data = await self.get_role_by_name(name=name)
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

    async def create_role(self, role_data: CreateRoleSchema) -> CreateRoleSchema:
        # TODO(Mosyagingrigorii): Подумать, как обернуть в транзакцию
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
        return role_data

    async def update_role(self, role_data: CreateRoleSchema) -> CreateRoleSchema | None:
        # TODO(Mosyagingrigorii): Подумать, как обернуть в транзакцию
        try:
            role = await self.get_role_by_name(name=role_data.role_name)
            action_names = [i[0] for i in role_data.actions if i[-1]]
            response_names = await self.actions_repo.get_actions_by_names(
                action_names=action_names
            )
            roles_ids = [row.id for row in response_names]
            await self.mixactions_repo.delete_actions_by_role(role_id=role.id)
            await self.mixactions_repo.set_actions_to_role(
                role_id=role.id, action_ids=roles_ids
            )
        except TypeError:
            return None
        return role_data


@lru_cache()
def get_role_service(
    roles_repo: RolesRepository = Depends(get_roles_repository),
    users_repo: UsersRepository = Depends(get_users_repository),
    actions_repo: ActionsRepository = Depends(get_actions_repository),
    mixactions_repo: MixActionsRepository = Depends(get_mix_actions_repository),
) -> RoleService:
    return RoleService(
        roles_repo=roles_repo,
        users_repo=users_repo,
        actions_repo=actions_repo,
        mixactions_repo=mixactions_repo,
    )
