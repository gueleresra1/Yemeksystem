from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # ← False yaptın mı?
    
    # Relationship
    role = relationship("Role", back_populates="users")
    foods = relationship("Food", back_populates="dealer") # dealer in yemekleri