# Migration Komutları

## Kurulum
```bash
# Virtual environment'ı aktif et
source venv/bin/activate

# Gerekli paketleri yükle (sadece ilk kez)
pip install alembic sqlalchemy
```

## Temel Migration Komutları

### 1. Yeni Migration Oluşturma
```bash
# Otomatik migration oluştur (model değişikliklerini algılar)
alembic revision --autogenerate -m "migration açıklaması"

# Manuel migration oluştur
alembic revision -m "migration açıklaması"
```

### 2. Migration'ları Uygulama
```bash
# Tüm migration'ları uygula
alembic upgrade head

# Belirli bir revision'a kadar uygula
alembic upgrade <revision_id>

# Bir sonraki migration'ı uygula
alembic upgrade +1
```

### 3. Migration'ları Geri Alma

# Son migration'ı geri al
alembic downgrade -1

# Belirli bir revision'a geri dön
alembic downgrade <revision_id>

# Tüm migration'ları geri al
alembic downgrade base
```

### 4. Migration Durumunu Kontrol Etme
```bash
# Mevcut revision'ı göster
alembic current

# Migration geçmişini göster
alembic history

# Uygulanmamış migration'ları göster
alembic show <revision_id>
```

## Örnek Workflow

### Yeni Model Ekleme
1. `models.py` dosyasına yeni model ekle
2. Migration oluştur: `alembic revision --autogenerate -m "add new model"`
3. Migration dosyasını kontrol et
4. Migration'ı uygula: `alembic upgrade head`

### Model Değişiklikleri
1. `models.py` dosyasında değişiklik yap
2. Migration oluştur: `alembic revision --autogenerate -m "update model"`
3. Migration dosyasını kontrol et
4. Migration'ı uygula: `alembic upgrade head`

### Prodüksiyon Deployment
```bash
# Önce backup al
cp users.db users.db.backup

# Migration'ları uygula
alembic upgrade head
```

## Önemli Notlar

- Migration dosyalarını her zaman kontrol edin
- Prodüksiyonda migration yapmadan önce backup alın
- Migration'ları test ortamında önce deneyin
- Geri alınamayan işlemler için dikkatli olun

## Dosya Yapısı
```
alembic/
├── env.py              # Alembic yapılandırması
├── script.py.mako      # Migration template
└── versions/           # Migration dosyaları
    └── xxxx_migration_name.py
```