from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Role
from auth import get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/dealer", tags=["dealer"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic modeli
class DealerRegister(BaseModel):
    email: str
    password: str

class DealerInfo(BaseModel):
    id: int
    email: str
    role: str
    message: str
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=DealerInfo)
def dealer_register(dealer_data: DealerRegister, db: Session = Depends(get_db)):
    """Yeni dealer/bayi kaydı"""
    
    # Email kontrolü
    existing_user = db.query(User).filter(User.email == dealer_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email adresi zaten kayıtlı"
        )
    
    # Dealer rolünü bul
    dealer_role = db.query(Role).filter(Role.name == "dealer").first()
    if not dealer_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Dealer rolü bulunamadı"
        )
    
    # Yeni dealer oluştur
    hashed_password = get_password_hash(dealer_data.password)
    new_dealer = User(
        email=dealer_data.email,
        password=hashed_password,
        role_id=dealer_role.id
    )
    
    db.add(new_dealer)
    db.commit()
    db.refresh(new_dealer)
    
    return DealerInfo(
        id=new_dealer.id,
        email=new_dealer.email,
        role=new_dealer.role.name,
        message=f"Dealer kaydı başarılı! Hoş geldin {new_dealer.email}"
    )