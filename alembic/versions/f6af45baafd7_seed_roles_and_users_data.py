"""Seed roles and users data

Revision ID: f6af45baafd7
Revises: 2053ac649a9b
Create Date: 2025-07-13 16:30:20.958289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6af45baafd7'
down_revision: Union[str, None] = '1bd036eee98b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from datetime import datetime
    import hashlib
    
    now = datetime.utcnow()
    
    # Roles tablosuna seed data ekleme
    roles_table = sa.table('roles',
        sa.column('name', sa.String),
        sa.column('description', sa.String),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime)
    )
    
    op.bulk_insert(roles_table, [
        {
            'name': 'admin',
            'description': 'System Administrator',
            'created_at': now,
            'updated_at': now
        },
        {
            'name': 'dealer',
            'description': 'Food Dealer/Restaurant Owner',
            'created_at': now,
            'updated_at': now
        },
        {
            'name': 'customer',
            'description': 'Customer/User',
            'created_at': now,
            'updated_at': now
        }
    ])
    
    # Role ID'lerini al
    connection = op.get_bind()
    admin_role_result = connection.execute(sa.text("SELECT id FROM roles WHERE name = 'admin'"))
    admin_role_id = admin_role_result.scalar()
    
    dealer_role_result = connection.execute(sa.text("SELECT id FROM roles WHERE name = 'dealer'"))
    dealer_role_id = dealer_role_result.scalar()
    
    customer_role_result = connection.execute(sa.text("SELECT id FROM roles WHERE name = 'customer'"))
    customer_role_id = customer_role_result.scalar()
    
    # Basit şifre hashleme (gerçek uygulamada bcrypt kullanın)
    def simple_hash(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # Users tablosuna seed data ekleme
    users_table = sa.table('users',
        sa.column('email', sa.String),
        sa.column('password', sa.String),
        sa.column('role_id', sa.Integer),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime)
    )
    
    op.bulk_insert(users_table, [
        {
            'email': 'admin@yemeksystem.com',
            'password': simple_hash('admin123'),
            'role_id': admin_role_id,
            'created_at': now,
            'updated_at': now
        },
        {
            'email': 'dealer1@yemeksystem.com',
            'password': simple_hash('dealer123'),
            'role_id': dealer_role_id,
            'created_at': now,
            'updated_at': now
        },
        {
            'email': 'dealer2@yemeksystem.com',
            'password': simple_hash('dealer123'),
            'role_id': dealer_role_id,
            'created_at': now,
            'updated_at': now
        },
        {
            'email': 'customer1@yemeksystem.com',
            'password': simple_hash('customer123'),
            'role_id': customer_role_id,
            'created_at': now,
            'updated_at': now
        }
    ])


def downgrade() -> None:
    # Users ve roles tablosundaki seed data'yı silme
    op.execute("DELETE FROM users WHERE email IN ('admin@yemeksystem.com', 'dealer1@yemeksystem.com', 'dealer2@yemeksystem.com', 'customer1@yemeksystem.com')")
    op.execute("DELETE FROM roles WHERE name IN ('admin', 'dealer', 'customer')")
