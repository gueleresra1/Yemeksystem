"""Seed comprehensive food translations data

Revision ID: 2053ac649a9b
Revises: 5275c141982b
Create Date: 2025-07-13 16:25:47.798636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2053ac649a9b'
down_revision: Union[str, None] = '5275c141982b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from datetime import datetime
    
    connection = op.get_bind()
    
    # Language ID'lerini al
    language_result = connection.execute(sa.text("SELECT id, code FROM languages ORDER BY id"))
    languages = {row[1]: row[0] for row in language_result}
    
    # Food ID'lerini ve isimlerini al
    food_result = connection.execute(sa.text("SELECT id, name FROM foods ORDER BY id"))
    foods = {row[1]: row[0] for row in food_result}
    
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
        
        # Kapsamlı çeviri verileri
        translations = {
            'Margherita Pizza': {
                'tr': {'name': 'Margherita Pizza', 'description': 'Klasik İtalyan pizzası - domates sosu, mozzarella ve fesleğen'},
                'en': {'name': 'Margherita Pizza', 'description': 'Classic Italian pizza with tomato sauce, mozzarella and basil'},
                'de': {'name': 'Margherita Pizza', 'description': 'Klassische italienische Pizza mit Tomatensoße, Mozzarella und Basilikum'},
                'fr': {'name': 'Pizza Margherita', 'description': 'Pizza italienne classique avec sauce tomate, mozzarella et basilic'},
                'es': {'name': 'Pizza Margherita', 'description': 'Pizza italiana clásica con salsa de tomate, mozzarella y albahaca'},
                'it': {'name': 'Pizza Margherita', 'description': 'Pizza italiana classica con salsa di pomodoro, mozzarella e basilico'}
            },
            'Cheeseburger': {
                'tr': {'name': 'Cheeseburger', 'description': 'Izgara köfte, cheddar peyniri, marul, domates'},
                'en': {'name': 'Cheeseburger', 'description': 'Grilled beef patty, cheddar cheese, lettuce, tomato'},
                'de': {'name': 'Cheeseburger', 'description': 'Gegrilltes Rindfleisch-Patty, Cheddar-Käse, Salat, Tomate'},
                'fr': {'name': 'Cheeseburger', 'description': 'Galette de bœuf grillée, fromage cheddar, laitue, tomate'},
                'es': {'name': 'Hamburguesa con Queso', 'description': 'Hamburguesa de carne a la parrilla, queso cheddar, lechuga, tomate'},
                'it': {'name': 'Cheeseburger', 'description': 'Hamburger di manzo grigliato, formaggio cheddar, lattuga, pomodoro'}
            },
            'Spaghetti Carbonara': {
                'tr': {'name': 'Spaghetti Carbonara', 'description': 'Kremalı İtalyan makarnası, pancetta ve parmesan'},
                'en': {'name': 'Spaghetti Carbonara', 'description': 'Creamy Italian pasta with pancetta and parmesan'},
                'de': {'name': 'Spaghetti Carbonara', 'description': 'Cremige italienische Pasta mit Pancetta und Parmesan'},
                'fr': {'name': 'Spaghetti Carbonara', 'description': 'Pâtes italiennes crémeuses avec pancetta et parmesan'},
                'es': {'name': 'Espaguetis Carbonara', 'description': 'Pasta italiana cremosa con pancetta y parmesano'},
                'it': {'name': 'Spaghetti alla Carbonara', 'description': 'Pasta italiana cremosa con pancetta e parmigiano'}
            },
            'Caesar Salad': {
                'tr': {'name': 'Caesar Salata', 'description': 'Taze marul, parmesan, kruton ve özel Caesar sosu'},
                'en': {'name': 'Caesar Salad', 'description': 'Fresh lettuce, parmesan, croutons and special Caesar dressing'},
                'de': {'name': 'Caesar Salat', 'description': 'Frischer Salat, Parmesan, Croutons und spezielle Caesar-Sauce'},
                'fr': {'name': 'Salade César', 'description': 'Laitue fraîche, parmesan, croûtons et vinaigrette César spéciale'},
                'es': {'name': 'Ensalada César', 'description': 'Lechuga fresca, parmesano, crutones y aderezo César especial'},
                'it': {'name': 'Insalata Caesar', 'description': 'Lattuga fresca, parmigiano, crostini e condimento Caesar speciale'}
            },
            'Grilled Chicken': {
                'tr': {'name': 'Izgara Tavuk', 'description': 'Izgara tavuk göğsü, sebze garnitürü ile'},
                'en': {'name': 'Grilled Chicken', 'description': 'Grilled chicken breast with vegetable garnish'},
                'de': {'name': 'Gegrilltes Hähnchen', 'description': 'Gegrillte Hähnchenbrust mit Gemüse-Beilage'},
                'fr': {'name': 'Poulet Grillé', 'description': 'Blanc de poulet grillé avec garniture de légumes'},
                'es': {'name': 'Pollo a la Parrilla', 'description': 'Pechuga de pollo a la parrilla con guarnición de verduras'},
                'it': {'name': 'Pollo alla Griglia', 'description': 'Petto di pollo grigliato con contorno di verdure'}
            },
            'Fish and Chips': {
                'tr': {'name': 'Fish and Chips', 'description': 'Çıtır balık ve patates kızartması'},
                'en': {'name': 'Fish and Chips', 'description': 'Crispy battered fish with french fries'},
                'de': {'name': 'Fish and Chips', 'description': 'Knuspriger Fisch im Teigmantel mit Pommes frites'},
                'fr': {'name': 'Fish and Chips', 'description': 'Poisson croustillant pané avec frites'},
                'es': {'name': 'Pescado con Patatas', 'description': 'Pescado crujiente rebozado con patatas fritas'},
                'it': {'name': 'Fish and Chips', 'description': 'Pesce croccante in pastella con patatine fritte'}
            },
            'Chocolate Cake': {
                'tr': {'name': 'Çikolatalı Kek', 'description': 'Evde yapılmış çikolatalı kek, vanilyalı dondurma ile'},
                'en': {'name': 'Chocolate Cake', 'description': 'Homemade chocolate cake with vanilla ice cream'},
                'de': {'name': 'Schokoladenkuchen', 'description': 'Hausgemachter Schokoladenkuchen mit Vanilleeis'},
                'fr': {'name': 'Gâteau au Chocolat', 'description': 'Gâteau au chocolat fait maison avec glace à la vanille'},
                'es': {'name': 'Pastel de Chocolate', 'description': 'Pastel de chocolate casero con helado de vainilla'},
                'it': {'name': 'Torta al Cioccolato', 'description': 'Torta al cioccolato fatta in casa con gelato alla vaniglia'}
            },
            'Tomato Soup': {
                'tr': {'name': 'Domates Çorbası', 'description': 'Ev yapımı domates çorbası, fesleğen ve krema ile'},
                'en': {'name': 'Tomato Soup', 'description': 'Homemade tomato soup with basil and cream'},
                'de': {'name': 'Tomatensuppe', 'description': 'Hausgemachte Tomatensuppe mit Basilikum und Sahne'},
                'fr': {'name': 'Soupe de Tomates', 'description': 'Soupe de tomates maison avec basilic et crème'},
                'es': {'name': 'Sopa de Tomate', 'description': 'Sopa de tomate casera con albahaca y crema'},
                'it': {'name': 'Zuppa di Pomodoro', 'description': 'Zuppa di pomodoro fatta in casa con basilico e panna'}
            }
        }
        
        translations_data = []
        
        for food_name, food_id in foods.items():
            if food_name in translations:
                for lang_code, lang_id in languages.items():
                    if lang_code in translations[food_name]:
                        translation = translations[food_name][lang_code]
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
    # Food translations tablosundaki seed data'yı silme
    connection = op.get_bind()
    
    # Seed food'ların ID'lerini al
    food_result = connection.execute(sa.text("SELECT id FROM foods WHERE name IN ('Margherita Pizza', 'Cheeseburger', 'Spaghetti Carbonara', 'Caesar Salad', 'Grilled Chicken', 'Fish and Chips', 'Chocolate Cake', 'Tomato Soup')"))
    food_ids = [str(row[0]) for row in food_result]
    
    if food_ids:
        op.execute(f"DELETE FROM food_translations WHERE food_id IN ({','.join(food_ids)})")
