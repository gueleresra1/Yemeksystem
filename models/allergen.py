from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

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
    translations = relationship("AllergenTranslation", back_populates="allergen")
    foods = relationship("Food", secondary=food_allergens, back_populates="allergens")
    recipes = relationship("Recipe", secondary=recipe_allergens, back_populates="allergens")

class AllergenTranslation(Base):
    __tablename__ = "allergen_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    allergen_id = Column(Integer, ForeignKey("allergens.id"), nullable=False)
    language_code = Column(String(5), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    allergen = relationship("Allergen", back_populates="translations")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('allergen_id', 'language_code'),
    )