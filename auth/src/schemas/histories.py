from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class HistoryBase(BaseModel):
    id: UUID = Field(comment="Идентификатор сессии пользователя")
    dt_login: datetime | None = Field(
        default=datetime.now(), comment="Дата и время входа пользователя"
    )
    dt_logout: datetime | None = Field(
        default=None, comment="Дата и время выхода пользователя"
    )
    user_id: UUID = Field(comment="Идентификатор пользователя")
    device_id: str | None = Field(
        default=None, comment="Идентификатор девайса пользователя"
    )
