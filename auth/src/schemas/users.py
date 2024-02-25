from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, validator

from .roles import RoleBaseSchema


class UserBaseSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(UserBaseSchema):
    hashed_password: str = Field(
        alias='password',
        description='User password',
    )


class FullUserSchema(UserBaseSchema):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    prone_number: str | None = None


class MixinCreateUserSchema(LoginUserSchema, FullUserSchema):
    pass


class UserDataInDBSchema(FullUserSchema):
    register_data: datetime


class UserDataToken(UserBaseSchema):
    token: UUID = Field(..., alias='access_token')
    id: UUID
    expires: datetime
    role: RoleBaseSchema
    token_type: Optional[str] = Field(default='bearer', description='Token type')

    @validator('token')
    def hexlify_token(cls, value):
        """Converts hex encoded token to."""
        return value.hex

    class Config:
        orm_mode = True
        populate_by_name = True


class UserResponseSchema(UserBaseSchema):
    token: UserDataToken = dict()
