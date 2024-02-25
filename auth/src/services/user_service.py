from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.sqlalchemy_repository import SQLAlchemyRepository

test_dict = {
    "email": ["admin", ],
    "password": ["admin", ]
}


class AuthUserService:
    async def get_user_by_email(
            self,
            database: AsyncSession,
            email: EmailStr
    ) -> list[str | None]:
        """Getting user object by email."""
        # TODO: delete after connect to repositories
        if False:
            result = await session.get(search=email)
            return result.scalar_one_or_none()
        else:
            result = test_dict.get('email')
            if result == email:
                return result
            return list()

    async def create_user(self):
        pass


user_service = AuthUserService()
