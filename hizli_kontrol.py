#!/usr/bin/env python3
"""
Hızlı veritabanı kontrol - Dosya oluşturmadan test
"""

try:
    from database import SessionLocal
    from sqlalchemy import text
    
    print("🔍 VERİTABANI HIZLI KONTROL")
    print("=" * 40)
    
    db = SessionLocal()
    
    # 1. Kullanıcı sayısı
    result = db.execute(text("SELECT COUNT(*) FROM users"))
    user_count = result.scalar()
    print(f"👥 Toplam kullanıcı: {user_count}")
    
    # 2. Timestamp kontrol
    print(f"\n🕒 TIMESTAMP DURUM:")
    result = db.execute(text("PRAGMA table_info(users)"))
    columns = [row[1] for row in result.fetchall()]
    
    has_created_at = 'created_at' in columns
    has_updated_at = 'updated_at' in columns
    
    print(f"created_at: {'✅ Var' if has_created_at else '❌ Yok'}")
    print(f"updated_at: {'✅ Var' if has_updated_at else '❌ Yok'}")
    
    if has_created_at and has_updated_at:
        print("\n🎉 BAŞARILI! Timestamp sistemi kuruldu!")
        
        # Örnek sorgu
        result = db.execute(text("SELECT email, created_at FROM users LIMIT 3"))
        print("\nÖrnek veriler:")
        for row in result.fetchall():
            print(f"  • {row[0]}: {row[1]}")
    else:
        print("\n❌ Timestamp'lar eksik")
    
    db.close()

except Exception as e:
    print(f"❌ Hata: {e}")