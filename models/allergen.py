from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

# Many-to-Many association tables
food_allergens = Table(
    'food_allergens',
    Base.metadata,
    Column('food_id', Integer, ForeignKey('foods.id'), primary_key=True),
    Column('allergen_id', Integer, ForeignKey('allergens.id'), primary_key=True)
)

recipe_allergens = Table(
    'recipe_allergens', 
    Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True),
    Column('allergen_id', Integer, ForeignKey('allergens.id'), primary_key=True)
)

class Allergen(Base):
    __tablename__ = "allergens"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    icon = Column(String, nullable=True)
    
    # Relationships
    foods = relationship("Food", secondary=food_allergens, back_populates="allergens")
    recipes = relationship("Recipe", secondary=recipe_allergens, back_populates="allergens")