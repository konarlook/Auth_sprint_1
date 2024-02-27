from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from schemas.roles import RoleBaseSchema


class UserBaseSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(UserBaseSchema):
    hashed_password: str


class FullUserSchema(UserBaseSchema):
    user_name: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)


class CreateUserSchema(LoginUserSchema, FullUserSchema):
    pass


class UserDataToken(UserBaseSchema):
    id: UUID
    role: RoleBaseSchema

    class Config:
        orm_mode = True
