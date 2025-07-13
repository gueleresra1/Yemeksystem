from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class FoodTranslation(Base):
    __tablename__ = "food_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    food = relationship("Food", back_populates="translations")
    language = relationship("Language", back_populates="food_translations")
    
    # Unique constraint - her food için her dil sadece bir çeviri
    __table_args__ = (
        UniqueConstraint('food_id', 'language_id'),
    )