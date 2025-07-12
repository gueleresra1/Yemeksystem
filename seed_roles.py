#!/usr/bin/env python3
# seed_roles.py - Başlangıç rollerini eklemek için

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Role

def create_default_roles():
    db = SessionLocal()
    try:
        # Mevcut rolleri kontrol et
        existing_roles = db.query(Role).all()
        if existing_roles:
            print("Roller zaten mevcut:")
            for role in existing_roles:
                print(f"- ID: {role.id}, Name: {role.name}, Description: {role.description}")
            return
        
        # Varsayılan rolleri oluştur
        roles = [
            Role(name="admin", description="Yönetici yetkisi"),
            Role(name="user", description="Normal kullanıcı"),
            Role(name="dealer", description="Bayi/Restorant yetkisi")
        ]
        
        for role in roles:
            db.add(role)
        
        db.commit()
        
        # Refresh yaparak ID'leri al
        for role in roles:
            db.refresh(role)
        
        print("✅ Varsayılan roller başarıyla oluşturuldu:")
        for role in roles:
            print(f"- ID: {role.id}, Name: {role.name}, Description: {role.description}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Hata: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        print("🔄 PostgreSQL bağlantısı kontrol ediliyor...")
        from database import engine
        with engine.connect() as connection:
            print("✅ PostgreSQL bağlantısı başarılı!")
        
        create_default_roles()
        
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        print("\n🔧 Çözüm önerileri:")
        print("1. Docker container'ın çalıştığından emin olun: docker-compose ps")
        print("2. Migration'ları çalıştırın: alembic upgrade head")
        print("3. PostgreSQL bağlantısını test edin: python database.py")   




        