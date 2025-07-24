from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, JSON
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
    tags = Column(JSON, nullable=True, default=[])  # Etiketler (JSON array)
    
    
    # Restaurant ve kategori bilgisi
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("restaurant_categories.id"), nullable=True)
    
    # Dealer bilgisi ve durum
    dealer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)  # Aktif/pasif
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="foods")
    category = relationship("RestaurantCategory", back_populates="foods")
    dealer = relationship("User", back_populates="foods")
    recipes = relationship("Recipe", back_populates="food", cascade="all, delete-orphan")
    allergens = relationship("Allergen", secondary="food_allergens", back_populates="foods")
    translations = relationship("FoodTranslation", back_populates="food", cascade="all, delete-orphan")