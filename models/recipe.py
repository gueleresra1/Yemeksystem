from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    
    # Reçete detayları
    ingredient_name = Column(String, nullable=False)  # Malzeme adı
    quantity = Column(String, nullable=False)  # Miktar (200gr, 1 adet, 2 çay kaşığı)
    step_order = Column(Integer, nullable=False)  # Yapım sırası
    instruction = Column(Text, nullable=True)  # Talimat (opsiyonel) # Malzeme bazli alerjenler
    
    # Relationship
    food = relationship("Food", back_populates="recipes")
    allergens = relationship("Allergen", secondary="recipe_allergens", back_populates="recipes")
