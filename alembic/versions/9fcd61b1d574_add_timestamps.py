# alembic/versions/9fcd61b1d574_add_timestamps.py dosyasını şöyle düzeltin:

"""add timestamps

Revision ID: 9fcd61b1d574
Revises: 4e6f581e135b
Create Date: 2025-07-11 XX:XX:XX.XXXXXX

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9fcd61b1d574'
down_revision: Union[str, None] = '4e6f581e135b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # SQLite uyumlu timestamp ekleme
    with op.batch_alter_table('users', schema=None) as batch_op:
        # server_default ile ekleme - SQLite uyumlu
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), 
                                     nullable=False, 
                                     server_default=sa.text('CURRENT_TIMESTAMP')))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), 
                                     nullable=False, 
                                     server_default=sa.text('CURRENT_TIMESTAMP')))

def downgrade() -> None:
    # Geri alma
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')