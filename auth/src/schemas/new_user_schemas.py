from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class BaseRequestSchema(BaseModel):
    email: EmailStr


class CreateUserRequestSchema(BaseRequestSchema):
    user_name: str | None = Field(default=None)
    password: str
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    phone_number: str | None = Field(default=None)


class CreateUserResponseSchema(BaseRequestSchema):
    dt_created: datetime


class LoginUserRequestSchema(BaseRequestSchema):
    password: str


class LoginUserResponseSchema(BaseRequestSchema):
    access_token: str
    refresh_token: str
    dt_login: datetime


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    dt_refresh: datetime


class LogoutRequestSchema(BaseModel):
    access_token: str
    refresh_token: str


class LogoutResponseSchema(BaseModel):
    dt_logout: datetime
