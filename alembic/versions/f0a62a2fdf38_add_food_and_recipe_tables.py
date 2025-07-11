"""add food and recipe tables

Revision ID: f0a62a2fdf38
Revises: 5381f805baa3
Create Date: 2025-07-10 15:18:34.372802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0a62a2fdf38'
down_revision: Union[str, None] = '5381f805baa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Food tablosunu oluştur
    op.create_table('foods',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('ingredients', sa.JSON(), nullable=False),
        sa.Column('allergens', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('dealer_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['dealer_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Recipe tablosunu oluştur
    op.create_table('recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('food_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_name', sa.String(), nullable=False),
        sa.Column('quantity', sa.String(), nullable=False),
        sa.Column('step_order', sa.Integer(), nullable=False),
        sa.Column('instruction', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['food_id'], ['foods.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('recipes')
    op.drop_table('foods')
