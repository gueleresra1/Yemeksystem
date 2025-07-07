# Authentication ve JWT Dokümantasyonu

## 📋 Genel Bakış

Bu sistem JWT (JSON Web Token) tabanlı kimlik doğrulama kullanır. Kullanıcılar email ve şifre ile giriş yapar, JWT token alır ve korumalı endpoint'lere erişim sağlar.

## 🔧 Kurulum ve Bağımlılıklar

```bash
# Virtual environment aktif et
source venv/bin/activate

# Gerekli paketler
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

## 🏗️ Sistem Mimarisi

### 1. Dosya Yapısı
```
├── auth.py          # JWT ve şifre yönetimi
├── main.py          # API endpoint'leri
├── schemas.py       # Pydantic modelleri
├── models.py        # SQLAlchemy modelleri
└── database.py      # Veritabanı bağlantısı
```

### 2. Temel Bileşenler

#### `auth.py` - Kimlik Doğrulama Modülü
- **Şifre Hashleme**: bcrypt ile güvenli şifre hashleme
- **JWT Token Yönetimi**: Token oluşturma, doğrulama
- **Kullanıcı Doğrulama**: Email/şifre kontrolü
- **Middleware**: Korumalı endpoint'ler için

#### `schemas.py` - Veri Modelleri
- **UserCreate**: Kullanıcı kayıt verisi
- **UserLogin**: Giriş verisi (email, password)
- **Token**: JWT token response
- **UserOut**: Güvenli kullanıcı bilgisi

## 🔐 Kimlik Doğrulama Süreci

### 1. Kullanıcı Kaydı
```http
POST /register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Süreç:**
1. Email/username benzersizlik kontrolü
2. Şifre bcrypt ile hashlenme
3. Kullanıcı veritabanına kaydedilme
4. Güvenli kullanıcı bilgisi dönülme

### 2. Giriş Yapma
```http
POST /login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

**Süreç:**
1. Email ile kullanıcı arama
2. Şifre doğrulama (bcrypt.verify)
3. JWT token oluşturma
4. Token ve tip dönülme

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Korumalı Endpoint'lere Erişim
```http
GET /users/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Süreç:**
1. Authorization header kontrolü
2. Bearer token çıkarma
3. JWT token doğrulama
4. Email ile kullanıcı bulma
5. Kullanıcı bilgisi dönülme

## 🛡️ Güvenlik Özellikleri

### 1. Şifre Güvenliği
- **bcrypt**: Endüstri standardı hashing
- **Salt**: Otomatik salt ekleme
- **Rounds**: Yeterli güvenlik seviyesi

### 2. JWT Token Güvenliği
- **Secret Key**: Güvenli imzalama anahtarı
- **Algorithm**: HS256 (HMAC-SHA256)
- **Expiration**: 30 dakika varsayılan
- **Claims**: Email (sub), expiration (exp)

### 3. HTTP Güvenliği
- **Bearer Token**: Standart authorization
- **CORS**: Cross-origin resource sharing
- **HTTPS**: Prodüksiyonda zorunlu

## 🔍 API Endpoint'leri

### 1. Genel Endpoint'ler
```http
GET /                    # Ana sayfa
```

### 2. Kimlik Doğrulama Endpoint'leri
```http
POST /register          # Kullanıcı kaydı
POST /login            # Giriş yapma
GET /users/me          # Mevcut kullanıcı bilgisi (korumalı)
```

### 3. Korumalı Endpoint'ler
```http
GET /protected         # Örnek korumalı endpoint
```

## 📝 Kullanım Örnekleri

### 1. Tam Workflow
```bash
# 1. Kullanıcı kaydı
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "password123"
  }'

# 2. Giriş yapma
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'

# 3. Token ile korumalı endpoint'e erişim
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 2. Python Client Örneği
```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Kullanıcı kaydı
register_data = {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "password123"
}
response = requests.post(f"{base_url}/register", json=register_data)
print(response.json())

# Giriş yapma
login_data = {
    "email": "john@example.com",
    "password": "password123"
}
response = requests.post(f"{base_url}/login", json=login_data)
token_data = response.json()
token = token_data["access_token"]

# Korumalı endpoint'e erişim
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(f"{base_url}/users/me", headers=headers)
print(response.json())
```

## ⚙️ Yapılandırma

### 1. Güvenlik Ayarları (auth.py)
```python
SECRET_KEY = "your-secret-key-here"  # Prodüksiyonda çevresel değişken
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 2. Önerilen Prodüksiyon Ayarları
```python
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))
```

## 🚨 Hata Yönetimi

### 1. Yaygın Hatalar
- **400**: Kullanıcı zaten mevcut
- **401**: Geçersiz kimlik bilgileri
- **401**: Geçersiz/süresi dolmuş token
- **422**: Geçersiz veri formatı

### 2. Hata Response Formatı
```json
{
  "detail": "Geçersiz email veya şifre"
}
```

## 🔧 Geliştirme İpuçları

### 1. Token Test Etme
```bash
# Token decode etmek için (jwt.io)
echo "YOUR_TOKEN" | base64 -d
```

### 2. Debugging
```python
# auth.py içinde debug log'ları
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 3. Token Yenileme
Şu anda token yenileme implementasyonu yok. Gelecekte refresh token eklenebilir.

## 🔒 Güvenlik Kontrol Listesi

- [x] Şifre hashleme (bcrypt)
- [x] JWT token imzalama
- [x] Token expiration
- [x] Bearer token authentication
- [x] CORS yapılandırması
- [ ] Rate limiting
- [ ] Refresh token
- [ ] Account lockout
- [ ] Password strength validation

## 📚 Referanslar

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/)
- [passlib Documentation](https://passlib.readthedocs.io/)
- [python-jose Documentation](https://python-jose.readthedocs.io/)