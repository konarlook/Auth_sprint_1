from pydantic import EmailStr

from .base_service import BaseService


class AuthUserService(BaseService):
    async def get(self, *, email: EmailStr):
        """Get user information by email."""
        pass

    async def create(self):
        """Create a new user by requesting email and password."""
        pass

    async def delete(self):
        """Delete user by email and password."""
        pass

    async def update(self):
        """Update user information."""
        pass


user_service = AuthUserService()
