from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL bağlantısı
DATABASE_URL = "postgresql://yemek_user:yemek123@localhost:5432/yemeksystem"

# PostgreSQL bağlantısı için optimize edilmiş ayarlar
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=20,
    max_overflow=10,
    echo=False,  # Debug için True yapabilirsiniz
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bağlantıyı test et
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ PostgreSQL bağlantısı başarılı!")
            result = connection.execute("SELECT version()")
            version = result.fetchone()[0]
            print(f"✅ PostgreSQL Version: {version}")
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        print("\n🔧 Çözüm önerileri:")
        print("1. Docker container'ın çalıştığından emin olun: docker-compose ps")
        print("2. PostgreSQL paketini yükleyin: pip install psycopg2-binary")
        print("3. Container'ı yeniden başlatın: docker-compose restart postgres")