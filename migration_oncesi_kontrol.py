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
    
    # 2. Rol sayısı
    try:
        result = db.execute(text("SELECT COUNT(*) FROM roles"))
        role_count = result.scalar()
        print(f"🎭 Toplam rol: {role_count}")
    except Exception as e:
        print(f"❌ Roles tablosu problemi: {e}")
        db.close()
        exit()
    
    # 3. Rolü olmayan kullanıcılar
    result = db.execute(text("SELECT COUNT(*) FROM users WHERE role_id IS NULL"))
    users_without_role = result.scalar()
    print(f"⚠️  Rolü olmayan kullanıcı: {users_without_role}")
    
    # 4. Durum analizi
    if users_without_role > 0:
        print(f"\n🚨 PROBLEM VAR!")
        print(f"{users_without_role} kullanıcının rolü yok!")
        print("role_id = nullable=False yaparsanız migration hatası verir!")
        
        # Rolü olmayan kullanıcıları göster
        result = db.execute(text("SELECT id, email FROM users WHERE role_id IS NULL LIMIT 5"))
        users = result.fetchall()
        
        print("\nÖrnek kullanıcılar:")
        for user in users:
            print(f"  • ID: {user[0]}, Email: {user[1]}")
        
        print(f"\n💡 ÇÖZÜMLERİ:")
        print("1. Bu kullanıcılara rol atayın")
        print("2. role_id = nullable=True bırakın") 
        print("3. Default rol atama scripti çalıştırın")
        
    else:
        print(f"\n✅ MÜKEMMEL!")
        print("Tüm kullanıcıların rolü var!")
        print("Migration güvenli, devam edebilirsiniz!")
    
    # 5. Rol dağılımı
    print(f"\n📊 ROL DAĞILIMI:")
    result = db.execute(text("""
        SELECT r.name, COUNT(u.id) as user_count
        FROM roles r
        LEFT JOIN users u ON r.id = u.role_id
        GROUP BY r.id, r.name
        ORDER BY user_count DESC
    """))
    
    for row in result.fetchall():
        role_name = row[0]
        count = row[1]
        print(f"  • {role_name}: {count} kullanıcı")
    
    # 6. Timestamp kontrol
    print(f"\n🕒 TIMESTAMP DURUM:")
    result = db.execute(text("PRAGMA table_info(users)"))
    columns = [row[1] for row in result.fetchall()]
    
    has_created_at = 'created_at' in columns
    has_updated_at = 'updated_at' in columns
    
    print(f"created_at: {'✅ Var' if has_created_at else '❌ Yok'}")
    print(f"updated_at: {'✅ Var' if has_updated_at else '❌ Yok'}")
    
    db.close()
    
    print(f"\n🎯 SONUÇ:")
    if users_without_role == 0:
        if not has_created_at:
            print("✅ Migration yapabilirsiniz!")
            print("Komutlar:")
            print("alembic revision --autogenerate -m 'add timestamps'")
            print("alembic upgrade head")
        else:
            print("✅ Timestamp zaten var, her şey tamam!")
    else:
        print("⚠️  Önce rol problemini çözün!")

except Exception as e:
    print(f"❌ Hata: {e}")
    print("Veritabanı bağlantısı sorunlu olabilir")