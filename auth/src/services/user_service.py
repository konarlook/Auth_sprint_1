from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Header, HTTPException, status

from models.auth_orm_models import UserDataOrm
from schemas.user import CreateUserSchema


class AuthUserService:
    async def get_user_by_token(
            self,
            token: str = Header(alias='access-token'),
    ) -> UserDataOrm:
        """Getting user authorization data by token"""
        if token not in ...:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='access token is invalid',
            )
