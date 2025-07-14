from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class RecipeTranslation(Base):
    __tablename__ = "recipe_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    ingredient_name = Column(String, nullable=False)
    instruction = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    recipe = relationship("Recipe", back_populates="translations")
    language = relationship("Language", back_populates="recipe_translations")
    
    # Unique constraint - her recipe için her dil sadece bir çeviri
    __table_args__ = (
        UniqueConstraint('recipe_id', 'language_id'),
    )