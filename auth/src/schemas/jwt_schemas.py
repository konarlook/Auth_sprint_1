from uuid import UUID, uuid4
from datetime import datetime
from .base import BaseSchema


class JWTSchema(BaseSchema):
    iat: int
    exp: int
    client_id: str
    jti: str


class AccessJWTSchema(JWTSchema):
    sub: UUID
    actions: list[str]


class RefreshJWTSchema(JWTSchema):
    id: str
