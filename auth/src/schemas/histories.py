from typing import List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class HistoryBase(BaseModel):
    id: UUID
    dt_login: List[datetime] | None
    dt_logout: List[datetime] | None
    user_id: UUID
    device_id: List[UUID] | None
