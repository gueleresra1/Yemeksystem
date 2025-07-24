"""seed_sample_foods_data

Revision ID: 015d392455d8
Revises: 61552a345449
Create Date: 2025-07-23 15:37:30.064216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '015d392455d8'
down_revision: Union[str, None] = '61552a345449'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Örnek foods verileri ekle
    from sqlalchemy import text
    
    # Dealer user'ı kontrol et (ID 3 role'ü dealer)
    connection = op.get_bind()
    
    # Örnek dealer kullanıcısı ekle (eğer yoksa)
    dealer_check = connection.execute(text("SELECT id FROM users WHERE role_id = 3 LIMIT 1")).fetchone()
    
    if not dealer_check:
        # Örnek dealer ekle
        connection.execute(text("""
            INSERT INTO users (email, password, role_id, created_at, updated_at) 
            VALUES ('dealer@test.com', '$2b$12$LQv3c1yqBwEHxE5W.IJLcuekjrRzMvRHSA4aZ9VWQo.ZZ8W5KCVwa', 3, NOW(), NOW())
        """))
    
    # Dealer ID'sini al
    dealer_result = connection.execute(text("SELECT id FROM users WHERE role_id = 3 LIMIT 1")).fetchone()
    dealer_id = dealer_result[0]
    
    # Örnek foods verileri ekle
    sample_foods = [
        # Ana Yemekler
        ("Adana Kebap", "Acılı dana kıyması ile hazırlanan geleneksel kebap", 85.00, "ana-yemek", dealer_id),
        ("Döner Kebap", "Özel baharatlarla marine edilmiş dana eti döner", 65.00, "ana-yemek", dealer_id),
        ("Izgara Köfte", "El yapımı köfte, mangal ateşinde ızgara", 70.00, "ana-yemek", dealer_id),
        ("Tavuk Şiş", "Marine edilmiş tavuk göğsü ızgara", 60.00, "ana-yemek", dealer_id),
        ("Karışık Izgara", "Adana, tavuk şiş, köfte karışımı", 95.00, "ana-yemek", dealer_id),
        
        # Aperativler
        ("Humus", "Nohut ezmesi, tahin, zeytinyağı", 25.00, "aperativ", dealer_id),
        ("Ezme", "Domates, biber, soğan, maydanoz", 20.00, "aperativ", dealer_id),
        ("Cacık", "Yoğurt, salatalık, sarımsak", 18.00, "aperativ", dealer_id),
        ("Közlenmiş Patlıcan", "Közlenmiş patlıcan salatası", 22.00, "aperativ", dealer_id),
        ("Sigara Böreği", "Peynirli, kızarmış börek", 30.00, "aperativ", dealer_id),
        
        # Tatlılar
        ("Baklava", "Fıstıklı geleneksel baklava", 35.00, "tatlilar", dealer_id),
        ("Künefe", "Kadayıf, peynir, şerbet", 40.00, "tatlilar", dealer_id),
        ("Sütlaç", "Fırında sütlaç", 25.00, "tatlilar", dealer_id),
        ("Kazandibi", "Geleneksel süt tatlısı", 28.00, "tatlilar", dealer_id),
        ("Revani", "Şerbetli revani tatlısı", 30.00, "tatlilar", dealer_id),
        
        # İçecekler
        ("Çay", "Geleneksel Türk çayı", 8.00, "icecekler", dealer_id),
        ("Türk Kahvesi", "Köpüklü Türk kahvesi", 15.00, "icecekler", dealer_id),
        ("Ayran", "Taze yoğurt ayranı", 12.00, "icecekler", dealer_id),
        ("Şalgam", "Acılı şalgam suyu", 10.00, "icecekler", dealer_id),
        ("Limonata", "Taze sıkılmış limon suyu", 18.00, "icecekler", dealer_id),
    ]
    
    for name, description, price, category, dealer_id in sample_foods:
        connection.execute(text("""
            INSERT INTO foods (name, description, price, category, dealer_id, is_active, created_at, updated_at)
            VALUES (:name, :description, :price, :category, :dealer_id, true, NOW(), NOW())
        """), {
            'name': name,
            'description': description, 
            'price': price,
            'category': category,
            'dealer_id': dealer_id
        })


def downgrade() -> None:
    # Örnek verileri sil
    from sqlalchemy import text
    connection = op.get_bind()
    
    # Örnek foods verilerini sil
    connection.execute(text("DELETE FROM foods WHERE name IN ('Adana Kebap', 'Döner Kebap', 'Izgara Köfte', 'Tavuk Şiş', 'Karışık Izgara', 'Humus', 'Ezme', 'Cacık', 'Közlenmiş Patlıcan', 'Sigara Böreği', 'Baklava', 'Künefe', 'Sütlaç', 'Kazandibi', 'Revani', 'Çay', 'Türk Kahvesi', 'Ayran', 'Şalgam', 'Limonata')"))
    
    # Test dealer'ı sil
    connection.execute(text("DELETE FROM users WHERE email = 'dealer@test.com'"))
