from uuid import UUID, uuid4
import orjson

from pydantic import BaseModel, Field


def orjson_dump(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseModelView(BaseModel):
    """Abstract base model for models of auth service"""

    id: UUID = Field(default_factory=uuid4)

    class Config:
        json_load = orjson.loads
        json_dumps = orjson_dump
