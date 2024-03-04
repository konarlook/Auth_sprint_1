"""add admin to user

Revision ID: 3955ac3a3742
Revises: 38b0347b107f
Create Date: 2024-03-04 19:51:01.752837

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from models.auth_orm_models import UserDataOrm, UsersOrm
from core.config import settings
from helpers.password import get_password_hash


# revision identifiers, used by Alembic.
revision: str = '3955ac3a3742'
down_revision: Union[str, None] = '38b0347b107f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    admin_id = str(uuid.uuid4())
    hashed_password = get_password_hash(settings.backend.auth_admin_password)
    op.bulk_insert(
        table=UserDataOrm.__table__,
        rows=[
            {
                "id": admin_id,
                "user_name": settings.backend.auth_admin_username,
                "hashed_password": hashed_password,
                "email": settings.backend.auth_admin_email,
            }
        ]
    )
    op.bulk_insert(
        table=UsersOrm.__table__,
        rows=[
            {
                "user_id": admin_id,
                "role_id": "25c245c4-1a06-42c7-bb55-0261a2f743d6",
            }
        ]
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text("DELETE FROM user_data;"))
    op.execute(sa.text("DELETE FROM users"))
    # ### end Alembic commands ###
