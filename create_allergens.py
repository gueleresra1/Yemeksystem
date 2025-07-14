#!/usr/bin/env python3
"""
Script to create allergen data in the database
"""

from sqlalchemy.orm import sessionmaker
from database import engine
from models.allergen import Allergen

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_allergens():
    """Create common allergen data"""
    session = SessionLocal()
    
    try:
        # Check if allergens already exist
        existing_count = session.query(Allergen).count()
        if existing_count > 0:
            print(f"Allergens already exist ({existing_count} records). Skipping creation.")
            return
        
        # Common allergens with codes and icons
        allergens_data = [
            {"id": 1, "code": "GLUTEN", "icon": "🌾"},
            {"id": 2, "code": "DAIRY", "icon": "🥛"},
            {"id": 3, "code": "EGGS", "icon": "🥚"},
            {"id": 4, "code": "NUTS", "icon": "🥜"},
            {"id": 5, "code": "PEANUTS", "icon": "🥜"},
            {"id": 6, "code": "SOY", "icon": "🫘"},
            {"id": 7, "code": "FISH", "icon": "🐟"},
            {"id": 8, "code": "SHELLFISH", "icon": "🦐"},
            {"id": 9, "code": "SESAME", "icon": "🫴"},
            {"id": 10, "code": "MUSTARD", "icon": "🟡"},
            {"id": 11, "code": "CELERY", "icon": "🥬"},
            {"id": 12, "code": "SULFITES", "icon": "🍷"},
            {"id": 13, "code": "LUPIN", "icon": "🌸"},
            {"id": 14, "code": "MOLLUSCS", "icon": "🐚"}
        ]
        
        # Create allergen records
        allergens = []
        for data in allergens_data:
            allergen = Allergen(
                id=data["id"],
                code=data["code"],
                icon=data["icon"]
            )
            allergens.append(allergen)
        
        # Add all allergens to the session
        session.add_all(allergens)
        session.commit()
        
        print(f"Successfully created {len(allergens)} allergens:")
        for allergen in allergens:
            print(f"  - {allergen.id}: {allergen.code} {allergen.icon}")
            
    except Exception as e:
        session.rollback()
        print(f"Error creating allergens: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    create_allergens()