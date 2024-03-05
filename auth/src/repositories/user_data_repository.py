import uuid
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from db.sqlalchemy_db import get_db_session
from models.auth_orm_models import UserDataOrm, RolesOrm, UsersOrm, MixActionsOrm, \
    ActionsOrm
from repositories.sqlalchemy_repository import SQLAlchemyRepository
from schemas.users import (
    CreateUserSchema,
    FullInfoUserSchema,
    MainInfoUserSchema,
)


class UserDataRepository(SQLAlchemyRepository):
    _model = UserDataOrm

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_user_by_email(self, email: str) -> FullInfoUserSchema | None:
        try:
            self._statement = select(self._model).where(self._model.email == email)
            raw_result = await self.read_one()
            result = self.to_pydantic(
                db_obj=raw_result, pydantic_model=FullInfoUserSchema
            )
        except NoResultFound:
            result = None
        return result

    async def get_user_by_id(self, user_id: UUID) -> MainInfoUserSchema | None:
        try:
            self._statement = select(self._model).where(self._model.id == user_id)
            raw_result = await self.read_one()
            result = self.to_pydantic(
                db_obj=raw_result, pydantic_model=MainInfoUserSchema
            )
        except NoResultFound:
            result = None
        return result

    async def get_user_by_username(self, username: str) -> MainInfoUserSchema | None:
        try:
            self._statement = select(self._model).where(
                self._model.user_name == username)
            raw_result = await self.read_one()
            result = self.to_pydantic(
                db_obj=raw_result, pydantic_model=MainInfoUserSchema,
            )
        except NoResultFound:
            result = None
        return result

    async def create_user(self, user_data: CreateUserSchema) -> dict:
        """Create user in database."""
        encode_data = jsonable_encoder(user_data)
        encode_data["id"] = uuid.uuid4()
        await self.create(encode_data)
        return encode_data

    async def update_password(
            self, user_id: str, new_password: str
    ):
        data = {'hashed_password': new_password}
        await self.update(
            orm_field=self._model.id, where_cond=user_id, update_data=data,
        )

    async def get_role_bu_user_id(self, user_id: UUID):
        role_subquery = select(UsersOrm.role_id).where(
            UsersOrm.user_id == user_id).subquery()

        actions_stmt = select(ActionsOrm.action_name).join(
            MixActionsOrm, MixActionsOrm.action_id == ActionsOrm.id
        ).where(
            MixActionsOrm.role_id == role_subquery.c.role_id
        )

        results = await self.session.execute(actions_stmt)
        action_names = results.scalars().all()

        return action_names


def get_database_client(session: AsyncSession = Depends(get_db_session)):
    return UserDataRepository(session=session)
