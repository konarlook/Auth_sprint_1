import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy_repository import SQLAlchemyRepository
from models.auth_orm_models import MixActionsOrm
from schemas.roles import MixActionSchema


class MixActionsRepository(SQLAlchemyRepository):
    _model = MixActionsOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def set_actions_to_role(
        self, role_id: uuid.UUID, action_ids: list[uuid.UUID]
    ):
        for action_id in action_ids:
            mix_actions_model = MixActionSchema(role_id=role_id, action_id=action_id)
            await self.insert(dict(mix_actions_model))

    async def update_actions_to_role(
        self, role_id: uuid.UUID, action_ids: list[uuid.UUID]
    ):
        for action_id in action_ids:
            mix_actions_model = MixActionSchema(role_id=role_id, action_id=action_id)
            await self.insert(dict(mix_actions_model))
