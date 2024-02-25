from uuid import UUID

from pydantic import BaseModel


class _BaseModel(BaseModel):
    id: UUID


class ActionsBaseSchema(_BaseModel):
    action_name: str
    comment: str


class RoleBaseSchema(_BaseModel):
    role_name: str
    comment: str
    actions: ActionsBaseSchema
