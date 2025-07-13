"""Seed food translations sample data

Revision ID: 1bd036eee98b
Revises: d9d02edb39c9
Create Date: 2025-07-13 16:23:01.164784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bd036eee98b'
down_revision: Union[str, None] = 'd9d02edb39c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Bu migration sadece mevcut food verisi varsa çalışır
    # Önce food ve language verilerinin olup olmadığını kontrol edelim
    
    from datetime import datetime
    
    # Food translations tablosuna örnek data ekleme
    # NOT: Bu migration gerçek food ve language ID'leri olduğunu varsayar
    # Eğer food tablosunda veri yoksa bu migration skip edilecek
    
    connection = op.get_bind()
    
    # Language ID'lerini al
    language_result = connection.execute(sa.text("SELECT id, code FROM languages ORDER BY id"))
    languages = {row[1]: row[0] for row in language_result}
    
    # Food ID'lerini al (sadece ilk birkaç food için örnek çeviri)
    food_result = connection.execute(sa.text("SELECT id, name FROM foods LIMIT 3"))
    foods = list(food_result)
    
    if foods and languages:
        food_translations_table = sa.table('food_translations',
            sa.column('food_id', sa.Integer),
            sa.column('language_id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('description', sa.Text),
            sa.column('created_at', sa.DateTime),
            sa.column('updated_at', sa.DateTime)
        )
        
        now = datetime.utcnow()
        translations_data = []
        
        # Örnek çeviriler - gerçek food adlarına göre adapte edilmeli
        sample_translations = {
            'tr': {
                'Pizza': {'name': 'Pizza', 'description': 'İtalyan mutfağından lezzetli pizza'},
                'Burger': {'name': 'Hamburger', 'description': 'Amerikden gelen lezzetli hamburger'},
                'Pasta': {'name': 'Makarna', 'description': 'İtalyan makarnası'}
            },
            'en': {
                'Pizza': {'name': 'Pizza', 'description': 'Delicious Italian pizza'},
                'Burger': {'name': 'Burger', 'description': 'Tasty American burger'},
                'Pasta': {'name': 'Pasta', 'description': 'Italian pasta dish'}
            },
            'de': {
                'Pizza': {'name': 'Pizza', 'description': 'Köstliche italienische Pizza'},
                'Burger': {'name': 'Burger', 'description': 'Leckerer amerikanischer Burger'},
                'Pasta': {'name': 'Pasta', 'description': 'Italienisches Pasta-Gericht'}
            }
        }
        
        for food_id, food_name in foods:
            for lang_code, lang_id in languages.items():
                if lang_code in sample_translations:
                    # Basit bir mapping - gerçek uygulamada daha sofistike olabilir
                    if 'pizza' in food_name.lower():
                        translation = sample_translations[lang_code].get('Pizza')
                    elif 'burger' in food_name.lower():
                        translation = sample_translations[lang_code].get('Burger')
                    elif 'pasta' in food_name.lower() or 'makarna' in food_name.lower():
                        translation = sample_translations[lang_code].get('Pasta')
                    else:
                        # Varsayılan çeviri
                        translation = {
                            'name': food_name,
                            'description': f'{food_name} - {lang_code.upper()} translation'
                        }
                    
                    if translation:
                        translations_data.append({
                            'food_id': food_id,
                            'language_id': lang_id,
                            'name': translation['name'],
                            'description': translation['description'],
                            'created_at': now,
                            'updated_at': now
                        })
        
        if translations_data:
            op.bulk_insert(food_translations_table, translations_data)


def downgrade() -> None:
    # Food translations tablosundaki örnek data'yı silme
    op.execute("DELETE FROM food_translations WHERE description LIKE '%translation%'")
