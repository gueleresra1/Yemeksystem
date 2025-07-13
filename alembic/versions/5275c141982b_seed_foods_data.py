"""Seed foods data

Revision ID: 5275c141982b
Revises: 1bd036eee98b
Create Date: 2025-07-13 16:25:12.857515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5275c141982b'
down_revision: Union[str, None] = 'f6af45baafd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from datetime import datetime
    
    connection = op.get_bind()
    
    # İlk dealer user ID'sini al (eğer varsa)
    user_result = connection.execute(sa.text("SELECT id FROM users WHERE role_id = (SELECT id FROM roles WHERE name = 'dealer') LIMIT 1"))
    user_row = user_result.fetchone()
    
    if not user_row:
        # Eğer dealer yoksa, herhangi bir user'ı al
        user_result = connection.execute(sa.text("SELECT id FROM users LIMIT 1"))
        user_row = user_result.fetchone()
    
    if user_row:
        dealer_id = user_row[0]
        
        foods_table = sa.table('foods',
            sa.column('name', sa.String),
            sa.column('description', sa.Text),
            sa.column('price', sa.Float),
            sa.column('category', sa.String),
            sa.column('dealer_id', sa.Integer),
            sa.column('is_active', sa.Boolean),
            sa.column('created_at', sa.DateTime),
            sa.column('updated_at', sa.DateTime)
        )
        
        now = datetime.utcnow()
        
        op.bulk_insert(foods_table, [
            {
                'name': 'Margherita Pizza',
                'description': 'Klasik İtalyan pizzası - domates sosu, mozzarella ve fesleğen',
                'price': 45.00,
                'category': 'Pizza',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Cheeseburger',
                'description': 'Izgara köfte, cheddar peyniri, marul, domates',
                'price': 35.00,
                'category': 'Burger',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Spaghetti Carbonara',
                'description': 'Kremalı İtalyan makarnası, pancetta ve parmesan',
                'price': 38.00,
                'category': 'Pasta',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Caesar Salad',
                'description': 'Taze marul, parmesan, kruton ve özel Caesar sosu',
                'price': 28.00,
                'category': 'Salata',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Grilled Chicken',
                'description': 'Izgara tavuk göğsü, sebze garnitürü ile',
                'price': 42.00,
                'category': 'Ana Yemek',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Fish and Chips',
                'description': 'Çıtır balık ve patates kızartması',
                'price': 48.00,
                'category': 'Ana Yemek',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Chocolate Cake',
                'description': 'Evde yapılmış çikolatalı kek, vanilyalı dondurma ile',
                'price': 22.00,
                'category': 'Tatlı',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            },
            {
                'name': 'Tomato Soup',
                'description': 'Ev yapımı domates çorbası, fesleğen ve krema ile',
                'price': 18.00,
                'category': 'Çorba',
                'dealer_id': dealer_id,
                'is_active': True,
                'created_at': now,
                'updated_at': now
            }
        ])


def downgrade() -> None:
    # Foods tablosundaki seed data'yı silme
    op.execute("DELETE FROM foods WHERE name IN ('Margherita Pizza', 'Cheeseburger', 'Spaghetti Carbonara', 'Caesar Salad', 'Grilled Chicken', 'Fish and Chips', 'Chocolate Cake', 'Tomato Soup')")
