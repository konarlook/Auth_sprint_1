import uuid
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from db.sqlalchemy_db import get_db_session
from models.auth_orm_models import UserDataOrm
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

    async def create_user(self, user_data: CreateUserSchema) -> dict:
        """Create user in database."""
        encode_data = jsonable_encoder(user_data)
        encode_data["id"] = uuid.uuid4()
        await self.create(encode_data)
        return encode_data


def get_database_client(session: AsyncSession = Depends(get_db_session)):
    return UserDataRepository(session=session)
