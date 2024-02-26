from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from models.auth_orm_models import RolesOrm, ActionsOrm, MixActionsOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from schemas.roles import RolesActionsSchema, RoleBaseSchema


class RolesRepository(SQLAlchemyRepository):
    _model = RolesOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_roles(self) -> list[RolesActionsSchema]:
        self._statement = (
            select(
                func.json_build_object(
                    "role_name",
                    RolesOrm.role_name,
                    "actions",
                    func.array_agg(
                        func.json_build_object(
                            "action_name",
                            ActionsOrm.action_name,
                            "comment",
                            ActionsOrm.comment,
                        )
                    ),
                )
            )
            .join(MixActionsOrm, RolesOrm.id == MixActionsOrm.role_id)
            .join(ActionsOrm, MixActionsOrm.action_id == ActionsOrm.id)
            .group_by(RolesOrm.role_name)
        )

        raw_result = await self.read()
        result = [RolesActionsSchema(**item) for item in raw_result]
        return result

    async def get_role_by_name(self, name: str) -> RoleBaseSchema | None:
        self._statement = select(RolesOrm).where(RolesOrm.role_name == name)
        result = await self.read_one()
        try:
            result = self.to_pydantic(result, RoleBaseSchema)
        except TypeError:
            result = None
        return result
