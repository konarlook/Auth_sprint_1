from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column


class BaseModelView(BaseModel):
    id: UUID = Field(default_factory=uuid4)