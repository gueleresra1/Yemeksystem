from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class AllergenTranslation(Base):
    __tablename__ = "allergen_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    name = Column(String, nullable=False)  # Çevrilmiş alerjen adı
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    allergen = relationship("Allergen", back_populates="translations")
    language = relationship("Language", back_populates="allergen_translations")
    
    # Unique constraint - her allergen için her dil sadece bir çeviri
    __table_args__ = (
        UniqueConstraint('allergen_id', 'language_id'),
    )