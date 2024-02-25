from typing import List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class _BaseModel(BaseModel):
    id: UUID


class ActionsBaseSchema(_BaseModel):
    action_name: str
    comment: str


class RoleBaseSchema(_BaseModel):
    role_name: str
    comment: str
    actions: ActionsBaseSchema


