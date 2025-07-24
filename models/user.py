from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # ← False yaptın mı?
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)    
    
    # Relationship
    role = relationship("Role", back_populates="users")
    foods = relationship("Food", back_populates="dealer") # dealer in yemekleri
    restaurants = relationship("Restaurant", back_populates="owner") # user'ın restoranları