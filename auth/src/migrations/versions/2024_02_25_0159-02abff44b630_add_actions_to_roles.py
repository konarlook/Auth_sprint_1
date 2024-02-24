"""add_actions_to_roles

Revision ID: 02abff44b630
Revises: 390888ecf4d3
Create Date: 2024-02-25 01:59:46.772739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from models.auth_orm_models import MixActionsOrm

# revision identifiers, used by Alembic.
revision: str = "02abff44b630"
down_revision: Union[str, None] = "390888ecf4d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(
        table=MixActionsOrm.__table__,
        rows=[
            {"id": 1, "role_id": 1, "action_id": 1},
            {"id": 2, "role_id": 1, "action_id": 2},
            {"id": 3, "role_id": 1, "action_id": 3},
            {"id": 4, "role_id": 1, "action_id": 4},
            {"id": 5, "role_id": 2, "action_id": 1},
            {"id": 6, "role_id": 2, "action_id": 2},
            {"id": 7, "role_id": 2, "action_id": 3},
            {"id": 8, "role_id": 2, "action_id": 5},
            {"id": 9, "role_id": 2, "action_id": 6},
            {"id": 10, "role_id": 2, "action_id": 7},
            {"id": 11, "role_id": 2, "action_id": 8},
            {"id": 12, "role_id": 2, "action_id": 9},
            {"id": 13, "role_id": 2, "action_id": 10},
            {"id": 14, "role_id": 2, "action_id": 11},
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text("DELETE FROM mix_actions;"))
    # ### end Alembic commands ###
