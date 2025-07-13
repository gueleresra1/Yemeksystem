"""Seed languages data

Revision ID: d9d02edb39c9
Revises: a5f037ae4a7a
Create Date: 2025-07-13 16:22:37.315137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9d02edb39c9'
down_revision: Union[str, None] = 'a5f037ae4a7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Languages tablosuna seed data ekleme
    languages_table = sa.table('languages',
        sa.column('code', sa.String),
        sa.column('name', sa.String),
        sa.column('native_name', sa.String),
        sa.column('is_active', sa.Boolean),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime)
    )
    
    from datetime import datetime
    now = datetime.utcnow()
    
    op.bulk_insert(languages_table, [
        {
            'code': 'tr',
            'name': 'Turkish',
            'native_name': 'Türkçe',
            'is_active': True,
            'created_at': now,
            'updated_at': now
        },
        {
            'code': 'en',
            'name': 'English',
            'native_name': 'English',
            'is_active': True,
            'created_at': now,
            'updated_at': now
        },
        {
            'code': 'de',
            'name': 'German',
            'native_name': 'Deutsch',
            'is_active': True,
            'created_at': now,
            'updated_at': now
        },
        {
            'code': 'fr',
            'name': 'French',
            'native_name': 'Français',
            'is_active': True,
            'created_at': now,
            'updated_at': now
        },
        {
            'code': 'es',
            'name': 'Spanish',
            'native_name': 'Español',
            'is_active': True,
            'created_at': now,
            'updated_at': now
        },
        {
            'code': 'it',
            'name': 'Italian',
            'native_name': 'Italiano',
            'is_active': True,
            'created_at': now,
            'updated_at': now
        }
    ])


def downgrade() -> None:
    # Languages tablosundaki seed data'yı silme
    op.execute("DELETE FROM languages WHERE code IN ('tr', 'en', 'de', 'fr', 'es', 'it')")
