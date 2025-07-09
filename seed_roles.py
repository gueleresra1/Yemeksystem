#!/usr/bin/env python3
# seed_roles.py - Başlangıç rollerini eklemek için

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Role

def create_default_roles():
    db = SessionLocal()
    try:
        # Varsayılan rolleri kontrol et
        existing_roles = db.query(Role).all()
        if existing_roles:
            print("Roller zaten mevcut:")
            for role in existing_roles:
                print(f"- {role.name}: {role.description}")
            return
        
        # Varsayılan rolleri oluştur
        roles = [
            Role(name="admin", description="Yönetici yetkisi"),
            Role(name="user", description="Normal kullanıcı"),
            Role(name="moderator", description="Moderatör yetkisi")
        ]
        
        for role in roles:
            db.add(role)
        
        db.commit()
        print("Varsayılan roller başarıyla oluşturuldu:")
        for role in roles:
            print(f"- {role.name}: {role.description}")
        
    except Exception as e:
        db.rollback()
        print(f"Hata: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_roles()