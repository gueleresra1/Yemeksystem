from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware (gerekirse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB oturumunu alma fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def sayGreeting():
    return "Hello Esra"

# 👤 User Register Endpoint
@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # E-posta veya kullanıcı adı zaten var mı?
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Benutzername oder E-Mail bereits vorhanden.")

    # Yeni kullanıcı oluştur
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password  # Normalde hash'lenmeli!
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
