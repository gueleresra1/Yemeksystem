"""add_tags_to_food_table

Revision ID: 61552a345449
Revises: c112c56e8da9
Create Date: 2025-07-20 13:45:31.769984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61552a345449'
down_revision: Union[str, None] = 'c112c56e8da9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('foods', sa.Column('tags', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('foods', 'tags')
    # ### end Alembic commands ###
