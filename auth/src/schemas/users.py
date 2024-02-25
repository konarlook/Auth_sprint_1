from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from .role import RoleBaseSchema


class UserBaseSchema(BaseModel):
    email: EmailStr


class LoginUserSchema(UserBaseSchema):
    hashed_password: str = Field(
        alias='password',
        description='User password',
    )


class FullUserSchema(UserBaseSchema):
    username: str
    first_name: str
    last_name: str
    # TODO: добавить валидацию номера
    prone_number: str


class MixinCreateUserSchema(LoginUserSchema, FullUserSchema):
    pass


class UserDataToken(UserBaseSchema):
    id: UUID
    role = RoleBaseSchema

    class Config:
        orm_mode = True


class UserDataInDBSchema(FullUserSchema):
    register_data: datetime
