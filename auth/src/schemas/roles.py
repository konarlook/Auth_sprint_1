import uuid

from pydantic import BaseModel, Field


class _BaseModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class ActionsBaseSchema(BaseModel):
    action_name: str
    comment: str


class RolesActionsSchema(BaseModel):
    role_name: str
    actions: list[ActionsBaseSchema]


class RoleBaseSchema(_BaseModel):
    role_name: str
    comment: str | None


class UsersRolesSchema(_BaseModel):
    user_id: uuid.UUID
    role_name: str


class Action_enum(BaseModel):
    logout: bool = Field(default=True)
    refresh_token: bool = Field(default=True)
    history: bool = Field(default=True)
    change_password: bool = Field(default=True)
    create_role: bool = Field(default=False)
    delete_role: bool = Field(default=False)
    change_role: bool = Field(default=False)
    get_roles: bool = Field(default=False)
    set_role: bool = Field(default=False)
    grab_role: bool = Field(default=False)
    check_role: bool = Field(default=False)


class CreateRoleSchema(BaseModel):
    role_name: str
    comment: str
    actions: Action_enum


class MixActionSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role_id: uuid.UUID
    action_id: uuid.UUID
