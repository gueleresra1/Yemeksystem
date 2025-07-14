from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class RoleTranslation(Base):
    __tablename__ = "role_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="translations")
    language = relationship("Language", back_populates="role_translations")
    
    # Unique constraint - her role için her dil sadece bir çeviri
    __table_args__ = (
        UniqueConstraint('role_id', 'language_id'),
    )