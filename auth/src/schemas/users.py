from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from schemas.roles import RoleBaseSchema


class UserBaseSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(UserBaseSchema):
    hashed_password: str


class LoginUserResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class FullUserSchema(UserBaseSchema):
    user_name: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)


class CreateUserSchema(LoginUserSchema, FullUserSchema):
    pass
