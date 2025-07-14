from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Language(Base):
    __tablename__ = "languages"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), unique=True, nullable=False, index=True)  # tr, en, de, fr, etc.
    name = Column(String, nullable=False)  # Turkish, English, German, French
    native_name = Column(String, nullable=True)  # Türkçe, English, Deutsch, Français
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    food_translations = relationship("FoodTranslation", back_populates="language")
    recipe_translations = relationship("RecipeTranslation", back_populates="language")
    allergen_translations = relationship("AllergenTranslation", back_populates="language")
    role_translations = relationship("RoleTranslation", back_populates="language")