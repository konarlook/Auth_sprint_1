from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(
        alias='password',
        description='User password',
    )


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(
        default=False,
        description='User activity status',
    )

    class Config:
        prm_model = True
