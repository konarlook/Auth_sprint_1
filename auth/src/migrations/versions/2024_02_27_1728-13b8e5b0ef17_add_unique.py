"""add_unique

Revision ID: 13b8e5b0ef17
Revises: 8a1bce43ed0d
Create Date: 2024-02-27 17:28:17.455437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision: str = "13b8e5b0ef17"
down_revision: Union[str, None] = "8a1bce43ed0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "actions", ["action_name"])
    op.create_unique_constraint(None, "roles", ["role_name"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "roles", type_="unique")
    op.drop_constraint(None, "actions", type_="unique")
    # ### end Alembic commands ###
