from pydantic import EmailStr
from fastapi import Depends

from .base_service import BaseService
from repositories.user_data_repository import get_database_client, UserDataRepository
from schemas.users import UserBaseSchema
from helpers.password import verify_password, get_password_hash


class AuthUserService(BaseService):
    def __init__(self, database_client: UserDataRepository):
        self.database_client = database_client

    async def get(self, *, email: EmailStr):
        """Get user information by email."""
        return await self.database_client.get_user_by_email(email)

    async def create(self, user_dto):
        """Create a new user by requesting email and password."""
        user_dto.hashed_password = get_password_hash(user_dto.hashed_password)
        await self.database_client.create_user(user_data=user_dto)
        return UserBaseSchema(email=user_dto.email)

    async def delete(self):
        """Delete user by email and password."""
        pass

    async def update(self):
        """Update user information."""
        pass

    async def check_user(self, user_info):
        response = await self.get(email=user_info.email)
        if not response:
            return None
        if not verify_password(
                user_info.hashed_password,
                response.hashed_password,
        ):
            return None
        return response


def get_user_service(
        database_client: UserDataRepository = Depends(get_database_client)):
    return AuthUserService(database_client=database_client)
