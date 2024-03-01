"""add_str_device_id

Revision ID: 38b0347b107f
Revises: 13b8e5b0ef17
Create Date: 2024-03-01 17:27:12.239270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "38b0347b107f"
down_revision: Union[str, None] = "13b8e5b0ef17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "auth_history",
        "device_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=256),
        comment="Устройства",
        existing_comment="ID устройства",
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "auth_history",
        "device_id",
        existing_type=sa.String(length=256),
        type_=sa.INTEGER(),
        comment="ID устройства",
        existing_comment="Устройства",
        existing_nullable=True,
    )
    # ### end Alembic commands ###