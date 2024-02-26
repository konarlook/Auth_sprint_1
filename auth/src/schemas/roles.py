from pydantic import BaseModel


class _BaseModel(BaseModel):
    id: int


class ActionsBaseSchema(BaseModel):
    action_name: str
    comment: str


class RolesActionsSchema(BaseModel):
    role_name: str
    actions: list[ActionsBaseSchema]


class RoleBaseSchema(_BaseModel):
    role_name: str
    comment: str
    actions: ActionsBaseSchema
