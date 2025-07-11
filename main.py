from fastapi import FastAPI
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, dealer, foods

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

# Routers'ı dahil et
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dealer.router)
app.include_router(foods.router)

@app.get("/")
def sayGreeting():
    return "Hello Esra"
