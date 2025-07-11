from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime 

class Food(Base):
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)  # Yemek adı
    description = Column(Text, nullable=True)  # Açıklama
    price = Column(Float, nullable=False)  # Fiyat
    category = Column(String, nullable=False)  # Kategori (Ana Yemek, Çorba, vs.)
    
    
    # Dealer bilgisi ve durum
    dealer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)  # Aktif/pasif
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    dealer = relationship("User", back_populates="foods")
    recipes = relationship("Recipe", back_populates="food", cascade="all, delete-orphan")
    allergens = relationship("Allergen", secondary="food_allergens", back_populates="foods")