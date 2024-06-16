"""Setup Roles

Revision ID: 548cdd92ed41
Revises: 0f18e18f9ae9
Create Date: 2024-06-16 14:36:40.496965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '548cdd92ed41'
down_revision: Union[str, None] = '0f18e18f9ae9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'quota')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('quota', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###